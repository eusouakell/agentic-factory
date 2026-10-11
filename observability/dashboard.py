from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from observability.metrics import load_events, summarize_portfolio


def _payload(events: list[dict]) -> dict:
    return summarize_portfolio(events)


def render_dashboard(payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agentic Factory — Observabilidade</title>
<style>
:root{{--ink:#101b2b;--muted:#637083;--line:#dfe4ea;--soft:#f5f7f9;--paper:#fff;--accent:#e65b15;--good:#176b45;--warn:#9a5b00;--bad:#a73737}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--soft);color:var(--ink);font:14px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
header{{background:var(--ink);color:white;padding:24px 32px}}header h1{{margin:0;font-size:22px}}header p{{margin:5px 0 0;color:#c6d0dc}}
main{{max-width:1500px;margin:auto;padding:24px 28px 56px}}.filters{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}}select{{border:1px solid var(--line);background:white;border-radius:8px;padding:9px 12px;min-width:180px}}
.kpis{{display:grid;grid-template-columns:repeat(6,minmax(140px,1fr));gap:12px;margin-bottom:24px}}.kpi{{background:white;border:1px solid var(--line);border-radius:10px;padding:16px}}.kpi small{{display:block;color:var(--muted);margin-bottom:5px}}.kpi strong{{font-size:26px;letter-spacing:-.03em}}
section{{background:white;border:1px solid var(--line);border-radius:12px;margin-top:16px;overflow:hidden}}section h2{{font-size:16px;margin:0;padding:16px 18px;border-bottom:1px solid var(--line)}}.section-body{{padding:16px 18px}}
table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;padding:10px 9px;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:12px;color:var(--muted);font-weight:600;background:#fafbfc;position:sticky;top:0}}.scroll{{overflow:auto;max-height:480px}}
.badge{{display:inline-block;border-radius:999px;padding:3px 8px;font-size:11px;background:#edf1f5}}.bad{{background:#fae8e8;color:var(--bad)}}.warn{{background:#fff0d8;color:var(--warn)}}.good{{background:#e3f4eb;color:var(--good)}}
.opportunity{{padding:12px 0;border-bottom:1px solid var(--line)}}.opportunity:last-child{{border:0}}.opportunity strong{{display:block;margin-bottom:3px}}.opportunity p{{margin:3px 0;color:#364354}}.empty{{color:var(--muted);padding:8px 0}}
.bar{{height:8px;background:#edf0f3;border-radius:999px;overflow:hidden;margin-top:8px}}.bar>span{{display:block;height:100%;background:var(--accent)}}
.meta{{color:var(--muted);font-size:12px}}@media(max-width:1000px){{.kpis{{grid-template-columns:repeat(3,1fr)}}}}@media(max-width:620px){{main{{padding:16px 12px 40px}}header{{padding:20px 16px}}.kpis{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>
<header><h1>Agentic Factory · Observabilidade</h1><p>Planejado × realizado, qualidade, retrabalho e atenção humana — com projeto como filtro.</p></header>
<main>
<div class="filters">
<select id="project"><option value="">Todos os projetos</option></select>
<select id="repo"><option value="">Todos os repositórios</option></select>
<select id="type"><option value="">Todos os workflows</option></select>
</div>
<div class="kpis" id="kpis"></div>
<section><h2>Plano × realizado</h2><div class="section-body"><div id="attainment"></div></div></section>
<section><h2>Oportunidades de melhoria</h2><div class="section-body" id="opportunities"></div></section>
<section><h2>Trabalho que saiu do previsto</h2><div class="scroll"><table><thead><tr><th>Projeto</th><th>Tipo</th><th>Tarefa</th><th>Pontos</th><th>Detalhe</th></tr></thead><tbody id="deviations"></tbody></table></div></section>
<section><h2>Workflows / runs</h2><div class="scroll"><table><thead><tr><th>Projeto</th><th>Workflow</th><th>Repo</th><th>Planejado</th><th>Aceito</th><th>Restante</th><th>Não planejado</th><th>Spillover</th><th>Retries</th><th>Qualidade</th><th>Tokens</th></tr></thead><tbody id="runs"></tbody></table></div></section>
</main>
<script>
const RAW={data};
const project=document.querySelector('#project'), repo=document.querySelector('#repo'), type=document.querySelector('#type');
const uniq=(xs)=>[...new Set(xs.filter(Boolean))].sort();
function fill(sel, values){{ for(const v of values){{const o=document.createElement('option');o.value=v;o.textContent=v;sel.appendChild(o)}} }}
fill(project,uniq(RAW.runs.map(x=>x.project_id)));fill(repo,uniq(RAW.runs.map(x=>x.repository)));fill(type,uniq(RAW.runs.map(x=>x.workflow_type)));
function fmtPct(v){{return Math.round((v||0)*100)+'%'}}function n(v){{return Number(v||0).toLocaleString('pt-BR')}}
function filteredRuns(){{return RAW.runs.filter(x=>(!project.value||x.project_id===project.value)&&(!repo.value||x.repository===repo.value)&&(!type.value||x.workflow_type===type.value))}}
function deriveOpp(runs){{
 const out=[]; if(!runs.length)return out;
 const totalPoints=runs.reduce((a,x)=>a+x.committed_points+x.unplanned_points,0);
 const unplanned=runs.reduce((a,x)=>a+x.unplanned_points,0);
 const spill=runs.reduce((a,x)=>a+x.spillover_points,0);
 const cycle=runs.reduce((a,x)=>a+x.cycle_seconds,0);
 const wait=runs.reduce((a,x)=>a+x.human_wait_seconds,0);
 const retries=runs.reduce((a,x)=>a+x.retries,0);
 const failed={{}}; runs.forEach(x=>Object.entries(x.failed_checks||{{}}).forEach(([k,v])=>failed[k]=(failed[k]||0)+v));
 if(totalPoints && unplanned/totalPoints>=.25) out.push({{signal:'High unplanned-work ratio',hypothesis:'Intake or planning may be incomplete before execution begins.',recommended_intervention:'Tighten intake/PRD completeness and record scope additions explicitly.',metric:'unplanned-work ratio',confidence:'medium'}});
 if(runs.reduce((a,x)=>a+x.committed_points,0) && spill>0) out.push({{signal:'Committed points spilled beyond target',hypothesis:'Capacity, dependencies or sizing may be miscalibrated.',recommended_intervention:'Inspect spillover tasks by point bucket and blocker/retry history.',metric:'spillover points',confidence:'medium'}});
 if(cycle && wait/cycle>=.4) out.push({{signal:'Human-wait share is high',hypothesis:'Human gates may be too frequent or positioned too early.',recommended_intervention:'Consolidate low-risk reviews behind meaningful decision gates.',metric:'human-wait ratio',confidence:'medium'}});
 if(retries) out.push({{signal:'Retry/revision loops detected',hypothesis:'Upstream acceptance criteria or handoffs may be underspecified.',recommended_intervention:'Trace retries to the earliest failed quality criterion and owning role.',metric:'retry rate / rework ratio',confidence:'medium'}});
 const ranked=Object.entries(failed).sort((a,b)=>b[1]-a[1]); if(ranked.length){{const [check,count]=ranked[0];out.push({{signal:'Recurring quality failure: '+check+' ('+count+'x)',hypothesis:'A repeatable quality weakness may exist upstream of the gate.',recommended_intervention:'Move the criterion earlier or strengthen the owning specialist handoff.',metric:'first-pass quality-gate pass rate',confidence:count>=3?'high':'medium'}})}}
 return out;
}}
function render(){{
 const runs=filteredRuns(); const ids=new Set(runs.map(x=>x.run_id));
 const committed=runs.reduce((a,x)=>a+x.committed_points,0), accepted=runs.reduce((a,x)=>a+x.accepted_planned_points,0), remaining=runs.reduce((a,x)=>a+x.remaining_planned_points,0), unplanned=runs.reduce((a,x)=>a+x.unplanned_points,0), spill=runs.reduce((a,x)=>a+x.spillover_points,0), retries=runs.reduce((a,x)=>a+x.retries,0), tokens=runs.reduce((a,x)=>a+x.usage.total_tokens,0);
 const attain=committed?accepted/committed:0;
 document.querySelector('#kpis').innerHTML=[
  ['Pontos planejados',n(committed)],['Pontos aceitos',n(accepted)],['Restante planejado',n(remaining)],['Não planejado',n(unplanned)],['Spillover real',n(spill)],['Tokens observados',n(tokens)]
 ].map(([a,b])=>'<div class="kpi"><small>'+a+'</small><strong>'+b+'</strong></div>').join('');
 document.querySelector('#attainment').innerHTML='<strong>'+n(accepted)+' / '+n(committed)+' pontos planejados aceitos</strong><div class="bar"><span style="width:'+Math.min(100,attain*100)+'%"></span></div><p class="meta">Pontos são sizing relativo; não são convertidos em horas.</p>';
 const deviations=RAW.deviations.filter(x=>ids.has(x.run_id));
 document.querySelector('#deviations').innerHTML=deviations.length?deviations.map(x=>'<tr><td>'+x.project_id+'</td><td><span class="badge '+(x.type==='quality'?'bad':x.type==='spillover'?'warn':'')+'">'+x.type+'</span></td><td>'+String(x.task_id||'—')+'</td><td>'+n(x.points)+'</td><td>'+x.detail+'</td></tr>').join(''):'<tr><td colspan="5" class="empty">Nenhum desvio registrado neste filtro.</td></tr>';
 document.querySelector('#runs').innerHTML=runs.length?runs.map(x=>'<tr><td>'+x.project_id+'</td><td>'+x.workflow_id+'</td><td>'+x.repository+'</td><td>'+n(x.committed_points)+'</td><td>'+n(x.accepted_planned_points)+'</td><td>'+n(x.remaining_planned_points)+'</td><td>'+n(x.unplanned_points)+'</td><td>'+n(x.spillover_points)+'</td><td>'+n(x.retries)+'</td><td>'+n(x.quality_gate_failures)+' falhas</td><td>'+n(x.usage.total_tokens)+' <span class="meta">'+x.usage_quality+'</span></td></tr>').join(''):'<tr><td colspan="11" class="empty">Ainda não há runs instrumentados para este filtro.</td></tr>';
 const opp=deriveOpp(runs);
 document.querySelector('#opportunities').innerHTML=opp.length?opp.map(x=>'<div class="opportunity"><strong>'+x.signal+'</strong><p>'+x.hypothesis+'</p><p><b>Ação sugerida:</b> '+x.recommended_intervention+'</p><span class="meta">Métrica: '+x.metric+' · confiança '+x.confidence+'</span></div>').join(''):'<div class="empty">Ainda não há sinal suficiente para gerar oportunidades.</div>';
}}
[project,repo,type].forEach(x=>x.addEventListener('change',render));render();
</script>
</body></html>"""


def build_dashboard(events_dir: Path, output: Path) -> Path:
    paths = sorted(events_dir.glob("*.jsonl")) if events_dir.exists() else []
    payload = _payload(load_events(paths))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dashboard(payload), encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", default="runs/events")
    parser.add_argument("--output", default="site/observability/index.html")
    args = parser.parse_args()
    output = build_dashboard(Path(args.events), Path(args.output))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

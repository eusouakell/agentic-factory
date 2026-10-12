from __future__ import annotations

import argparse
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
main{{max-width:1600px;margin:auto;padding:24px 28px 56px}}.filters{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}}
select{{border:1px solid var(--line);background:white;border-radius:8px;padding:9px 12px;min-width:180px}}
.kpis{{display:grid;grid-template-columns:repeat(5,minmax(140px,1fr));gap:12px;margin-bottom:24px}}
.kpi{{background:white;border:1px solid var(--line);border-radius:10px;padding:16px}}.kpi small{{display:block;color:var(--muted);margin-bottom:5px}}.kpi strong{{font-size:25px;letter-spacing:-.03em}}
section{{background:white;border:1px solid var(--line);border-radius:12px;margin-top:16px;overflow:hidden}}section h2{{font-size:16px;margin:0;padding:16px 18px;border-bottom:1px solid var(--line)}}.section-body{{padding:16px 18px}}
table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;padding:10px 9px;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:12px;color:var(--muted);font-weight:600;background:#fafbfc;position:sticky;top:0;z-index:1}}
.scroll{{overflow:auto;max-height:480px}}.wide{{min-width:980px}}
.badge{{display:inline-block;border-radius:999px;padding:3px 8px;font-size:11px;background:#edf1f5}}.bad{{background:#fae8e8;color:var(--bad)}}.warn{{background:#fff0d8;color:var(--warn)}}.good{{background:#e3f4eb;color:var(--good)}}
.opportunity{{padding:12px 0;border-bottom:1px solid var(--line)}}.opportunity:last-child{{border:0}}.opportunity strong{{display:block;margin-bottom:3px}}.opportunity p{{margin:3px 0;color:#364354}}
.empty{{color:var(--muted);padding:8px 0}}.bar{{height:8px;background:#edf0f3;border-radius:999px;overflow:hidden;margin-top:8px}}.bar>span{{display:block;height:100%;background:var(--accent)}}.meta{{color:var(--muted);font-size:12px}}
.board-state{{font-weight:600}}.accepted{{color:var(--good)}}.running{{color:var(--warn)}}.failed{{color:var(--bad)}}
.note{{margin:8px 0 0;color:var(--muted);font-size:12px}}
@media(max-width:1050px){{.kpis{{grid-template-columns:repeat(3,1fr)}}}}
@media(max-width:620px){{main{{padding:16px 12px 40px}}header{{padding:20px 16px}}.kpis{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>
<header>
  <h1>Agentic Factory · Observabilidade</h1>
  <p>Planejado × realizado, fluxo, qualidade, A2 e gates humanos — com projeto como filtro.</p>
</header>
<main>
<div class="filters">
<select id="project"><option value="">Todos os projetos</option></select>
<select id="repo"><option value="">Todos os repositórios</option></select>
<select id="type"><option value="">Todos os workflows</option></select>
</div>

<div class="kpis" id="kpis"></div>

<section><h2>Plano × realizado</h2><div class="section-body"><div id="attainment"></div></div></section>

<section><h2>Fluxo e eficiência</h2>
<div class="scroll"><table class="wide"><thead><tr>
<th>Projeto</th><th>Workflow</th><th>Ciclo</th><th>Ativo</th><th>Wait em gate</th><th>Eficiência</th><th>Retrabalho</th><th>Retries</th><th>A2 execuções</th>
</tr></thead><tbody id="flow"></tbody></table></div>
<div class="section-body"><p class="note">Wait em gate é tempo decorrido entre abertura e resolução do gate; não representa atenção humana ativa.</p></div>
</section>

<section><h2>Board operacional derivado dos eventos</h2>
<div class="scroll"><table class="wide"><thead><tr>
<th>Projeto</th><th>Tarefa</th><th>Agente</th><th>Estado</th><th>Pontos</th><th>Origem</th><th>Grupo paralelo</th><th>Dependências</th><th>Tentativas</th>
</tr></thead><tbody id="board"></tbody></table></div>
</section>

<section><h2>Timeline normalizada</h2>
<div class="scroll"><table class="wide"><thead><tr>
<th>Quando</th><th>Projeto</th><th>Evento</th><th>Tarefa</th><th>Agente</th><th>Gate / execução / critério</th>
</tr></thead><tbody id="timeline"></tbody></table></div>
</section>

<section><h2>Qualidade · hotspots e escaped defects</h2>
<div class="scroll"><table><thead><tr><th>Check</th><th>Falhas/unknown</th></tr></thead><tbody id="quality"></tbody></table></div>
</section>

<section><h2>Comparação por agente</h2>
<div class="scroll"><table class="wide"><thead><tr>
<th>Agente</th><th>Projetos</th><th>Tasks iniciadas</th><th>Concluídas</th><th>Retries</th><th>Tempo ativo</th><th>Retrabalho</th><th>A2 ok</th><th>A2 falhas</th><th>Tokens</th>
</tr></thead><tbody id="agents"></tbody></table></div>
</section>

<section><h2>Comparação por projeto</h2>
<div class="scroll"><table class="wide"><thead><tr>
<th>Projeto</th><th>Runs</th><th>Planejado</th><th>Aceito</th><th>Não planejado</th><th>Spillover</th><th>Eficiência</th><th>Wait em gate</th><th>Retrabalho</th><th>Falhas de gate</th><th>Escaped defects</th>
</tr></thead><tbody id="projects"></tbody></table></div>
</section>

<section><h2>Oportunidades de melhoria</h2><div class="section-body" id="opportunities"></div></section>

<section><h2>Trabalho que saiu do previsto</h2>
<div class="scroll"><table><thead><tr><th>Projeto</th><th>Tipo</th><th>Tarefa</th><th>Pontos</th><th>Detalhe</th></tr></thead><tbody id="deviations"></tbody></table></div>
</section>

<section><h2>Workflows / runs</h2>
<div class="scroll"><table class="wide"><thead><tr>
<th>Projeto</th><th>Workflow</th><th>Repo</th><th>Planejado</th><th>Aceito</th><th>Restante</th><th>Não planejado</th><th>Spillover</th><th>Convergência</th><th>Humano</th><th>Qualidade</th><th>Escaped</th><th>Tokens</th>
</tr></thead><tbody id="runs"></tbody></table></div>
</section>
</main>

<script>
const RAW={data};
const project=document.querySelector('#project'), repo=document.querySelector('#repo'), type=document.querySelector('#type');
const uniq=(xs)=>[...new Set(xs.filter(Boolean))].sort();
const esc=(v)=>String(v??'—').replace(/[&<>"']/g,ch=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
const n=(v)=>Number(v||0).toLocaleString('pt-BR');
const sec=(v)=>{{const x=Number(v||0);return x>=3600?(x/3600).toFixed(1)+'h':x>=60?(x/60).toFixed(1)+'m':x.toFixed(1)+'s'}};
const pct=(v)=>Math.round(Number(v||0)*100)+'%';
function fill(sel, values){{for(const v of values){{const o=document.createElement('option');o.value=v;o.textContent=v;sel.appendChild(o)}}}}
fill(project,uniq(RAW.runs.map(x=>x.project_id)));fill(repo,uniq(RAW.runs.map(x=>x.repository)));fill(type,uniq(RAW.runs.map(x=>x.workflow_type)));
function filteredRuns(){{return RAW.runs.filter(x=>(!project.value||x.project_id===project.value)&&(!repo.value||x.repository===repo.value)&&(!type.value||x.workflow_type===type.value))}}

function deriveOpp(runs){{
 const out=[]; if(!runs.length)return out;
 const totalPoints=runs.reduce((a,x)=>a+x.committed_points+x.unplanned_points,0);
 const unplanned=runs.reduce((a,x)=>a+x.unplanned_points,0);
 const spill=runs.reduce((a,x)=>a+x.spillover_points,0);
 const cycle=runs.reduce((a,x)=>a+x.cycle_seconds,0);
 const wait=runs.reduce((a,x)=>a+x.human_wait_seconds,0);
 const retries=runs.reduce((a,x)=>a+x.retries,0);
 const escaped=runs.reduce((a,x)=>a+(x.escaped_defects||0),0);
 const failed={{}};runs.forEach(x=>Object.entries(x.failed_checks||{{}}).forEach(([k,v])=>failed[k]=(failed[k]||0)+v));
 if(totalPoints&&unplanned/totalPoints>=.25)out.push({{signal:'High unplanned-work ratio',hypothesis:'Intake ou planejamento podem estar incompletos.',recommended_intervention:'Apertar intake/PRD e registrar adições de escopo.',metric:'unplanned-work ratio',confidence:'medium'}});
 if(runs.reduce((a,x)=>a+x.committed_points,0)&&spill>0)out.push({{signal:'Committed points spilled beyond target',hypothesis:'Capacidade, dependências ou sizing podem estar descalibrados.',recommended_intervention:'Inspecionar tarefas com spillover por retry/bloqueio.',metric:'spillover points',confidence:'medium'}});
 if(cycle&&wait/cycle>=.4)out.push({{signal:'Human-gate wait share is high',hypothesis:'Gates podem estar frequentes ou cedo demais.',recommended_intervention:'Consolidar reviews de baixo risco atrás de gates significativos.',metric:'human-wait ratio',confidence:'medium'}});
 if(retries)out.push({{signal:'Retry/revision loops detected',hypothesis:'Critérios upstream ou handoffs podem estar subespecificados.',recommended_intervention:'Rastrear retries até o primeiro critério e owner que falhou.',metric:'retry rate / rework ratio',confidence:'medium'}});
 if(escaped)out.push({{signal:'Escaped defects detected ('+escaped+')',hypothesis:'Um estágio posterior encontrou defeito material não capturado upstream.',recommended_intervention:'Mover/reforçar o critério no gate owning antes do próximo piloto.',metric:'escaped defect count',confidence:'high'}});
 const ranked=Object.entries(failed).sort((a,b)=>b[1]-a[1]);if(ranked.length){{const [check,count]=ranked[0];out.push({{signal:'Recurring quality failure: '+check+' ('+count+'x)',hypothesis:'Há uma fraqueza repetível antes do gate.',recommended_intervention:'Mover o critério para mais cedo ou fortalecer o handoff do owner.',metric:'first-pass quality-gate pass rate',confidence:count>=3?'high':'medium'}})}}
 return out;
}}

function agentRows(runs){{
 const m={{}};
 runs.forEach(run=>(run.agent_metrics||[]).forEach(a=>{{
   const row=m[a.agent_id]||(m[a.agent_id]={{agent_id:a.agent_id,projects:new Set(),tasks_started:0,tasks_completed:0,retries:0,active_seconds:0,rework_seconds:0,agent_executions_completed:0,agent_executions_failed:0,tokens_observed:0}});
   row.projects.add(run.project_id);
   ['tasks_started','tasks_completed','retries','active_seconds','rework_seconds','agent_executions_completed','agent_executions_failed','tokens_observed'].forEach(k=>row[k]+=Number(a[k]||0));
 }}));
 return Object.values(m).sort((a,b)=>a.agent_id.localeCompare(b.agent_id));
}}

function projectRows(runs){{
 const m={{}};
 runs.forEach(run=>{{
  const row=m[run.project_id]||(m[run.project_id]={{project_id:run.project_id,workflow_count:0,committed_points:0,accepted_planned_points:0,unplanned_points:0,spillover_points:0,cycle_seconds:0,active_seconds:0,human_wait_seconds:0,rework_seconds:0,quality_gate_failures:0,escaped_defects:0}});
  row.workflow_count++; row.committed_points+=run.committed_points;row.accepted_planned_points+=run.accepted_planned_points;row.unplanned_points+=run.unplanned_points;row.spillover_points+=run.spillover_points;row.cycle_seconds+=run.cycle_seconds;row.active_seconds+=run.active_seconds;row.human_wait_seconds+=run.human_wait_seconds;row.rework_seconds+=run.rework_seconds;row.quality_gate_failures+=run.quality_gate_failures;row.escaped_defects+=run.escaped_defects||0;
 }});
 return Object.values(m).map(row=>({{...row,flow_efficiency:row.cycle_seconds?row.active_seconds/row.cycle_seconds:0}})).sort((a,b)=>a.project_id.localeCompare(b.project_id));
}}

function render(){{
 const runs=filteredRuns();const ids=new Set(runs.map(x=>x.run_id));
 const committed=runs.reduce((a,x)=>a+x.committed_points,0),accepted=runs.reduce((a,x)=>a+x.accepted_planned_points,0),remaining=runs.reduce((a,x)=>a+x.remaining_planned_points,0),unplanned=runs.reduce((a,x)=>a+x.unplanned_points,0),spill=runs.reduce((a,x)=>a+x.spillover_points,0),tokens=runs.reduce((a,x)=>a+x.usage.total_tokens,0),cycle=runs.reduce((a,x)=>a+x.cycle_seconds,0),active=runs.reduce((a,x)=>a+x.active_seconds,0),wait=runs.reduce((a,x)=>a+x.human_wait_seconds,0),rework=runs.reduce((a,x)=>a+x.rework_seconds,0),escaped=runs.reduce((a,x)=>a+(x.escaped_defects||0),0);
 const attain=committed?accepted/committed:0,flow=cycle?active/cycle:0;
 document.querySelector('#kpis').innerHTML=[
  ['Planejado',n(committed)],['Aceito',n(accepted)],['Restante',n(remaining)],['Não planejado',n(unplanned)],['Spillover',n(spill)],
  ['Eficiência',pct(flow)],['Wait em gate',sec(wait)],['Retrabalho',sec(rework)],['Escaped defects',n(escaped)],['Tokens observados',n(tokens)]
 ].map(([a,b])=>'<div class="kpi"><small>'+esc(a)+'</small><strong>'+esc(b)+'</strong></div>').join('');
 document.querySelector('#attainment').innerHTML='<strong>'+n(accepted)+' / '+n(committed)+' pontos planejados aceitos</strong><div class="bar"><span style="width:'+Math.min(100,attain*100)+'%"></span></div><p class="meta">Sizing relativo: 1/2/3/5/8. Não há conversão automática de pontos para horas.</p>';

 document.querySelector('#flow').innerHTML=runs.length?runs.map(x=>'<tr><td>'+esc(x.project_id)+'</td><td>'+esc(x.workflow_id)+'</td><td>'+sec(x.cycle_seconds)+'</td><td>'+sec(x.active_seconds)+'</td><td>'+sec(x.human_wait_seconds)+'</td><td>'+pct(x.flow_efficiency)+'</td><td>'+sec(x.rework_seconds)+' <span class="meta">'+pct(x.rework_ratio)+'</span></td><td>'+n(x.retries)+'</td><td>'+n(x.agent_executions_completed)+' ok / '+n(x.agent_executions_failed)+' falhas</td></tr>').join(''):'<tr><td colspan="9" class="empty">Sem runs neste filtro.</td></tr>';

 const board=runs.flatMap(x=>(x.board||[]).map(t=>({{...t,project_id:x.project_id,run_id:x.run_id}})));
 document.querySelector('#board').innerHTML=board.length?board.map(t=>'<tr><td>'+esc(t.project_id)+'</td><td>'+esc(t.task_id)+'</td><td>'+esc(t.agent_id)+'</td><td><span class="board-state '+esc(t.state)+'">'+esc(t.state)+'</span></td><td>'+n(t.sizing_points)+'</td><td>'+esc(t.planning_origin)+'</td><td>'+esc(t.parallel_group)+'</td><td>'+esc((t.depends_on||[]).join(', ')||'—')+'</td><td>'+n(t.attempts)+'</td></tr>').join(''):'<tr><td colspan="9" class="empty">Sem tarefas projetadas.</td></tr>';

 const timeline=runs.flatMap(x=>(x.timeline||[]).map(e=>({{...e,project_id:x.project_id}}))).sort((a,b)=>String(b.timestamp).localeCompare(String(a.timestamp))).slice(0,250);
 document.querySelector('#timeline').innerHTML=timeline.length?timeline.map(e=>'<tr><td>'+esc(e.timestamp)+'</td><td>'+esc(e.project_id)+'</td><td>'+esc(e.event_type)+'</td><td>'+esc(e.task_id)+'</td><td>'+esc(e.agent_id)+'</td><td>'+esc(e.gate_id||e.execution_id||e.criterion||'—')+'</td></tr>').join(''):'<tr><td colspan="6" class="empty">Sem eventos normalizados.</td></tr>';

 const failed={{}};runs.forEach(x=>Object.entries(x.failed_checks||{{}}).forEach(([k,v])=>failed[k]=(failed[k]||0)+v));
 const hotspots=Object.entries(failed).sort((a,b)=>b[1]-a[1]);
 document.querySelector('#quality').innerHTML=hotspots.length?hotspots.map(([k,v])=>'<tr><td>'+esc(k)+'</td><td>'+n(v)+'</td></tr>').join(''):'<tr><td colspan="2" class="empty">Nenhum hotspot de qualidade neste filtro.</td></tr>';

 const agents=agentRows(runs);
 document.querySelector('#agents').innerHTML=agents.length?agents.map(a=>'<tr><td>'+esc(a.agent_id)+'</td><td>'+esc([...a.projects].sort().join(', '))+'</td><td>'+n(a.tasks_started)+'</td><td>'+n(a.tasks_completed)+'</td><td>'+n(a.retries)+'</td><td>'+sec(a.active_seconds)+'</td><td>'+sec(a.rework_seconds)+'</td><td>'+n(a.agent_executions_completed)+'</td><td>'+n(a.agent_executions_failed)+'</td><td>'+n(a.tokens_observed)+'</td></tr>').join(''):'<tr><td colspan="10" class="empty">Sem atividade atribuída a agentes.</td></tr>';

 const projects=projectRows(runs);
 document.querySelector('#projects').innerHTML=projects.length?projects.map(p=>'<tr><td>'+esc(p.project_id)+'</td><td>'+n(p.workflow_count)+'</td><td>'+n(p.committed_points)+'</td><td>'+n(p.accepted_planned_points)+'</td><td>'+n(p.unplanned_points)+'</td><td>'+n(p.spillover_points)+'</td><td>'+pct(p.flow_efficiency)+'</td><td>'+sec(p.human_wait_seconds)+'</td><td>'+sec(p.rework_seconds)+'</td><td>'+n(p.quality_gate_failures)+'</td><td>'+n(p.escaped_defects)+'</td></tr>').join(''):'<tr><td colspan="11" class="empty">Sem projetos neste filtro.</td></tr>';

 const opp=deriveOpp(runs);
 document.querySelector('#opportunities').innerHTML=opp.length?opp.map(x=>'<div class="opportunity"><strong>'+esc(x.signal)+'</strong><p>'+esc(x.hypothesis)+'</p><p><b>Ação sugerida:</b> '+esc(x.recommended_intervention)+'</p><span class="meta">Métrica: '+esc(x.metric)+' · confiança '+esc(x.confidence)+'</span></div>').join(''):'<div class="empty">Ainda não há sinal suficiente para gerar oportunidades.</div>';

 const deviations=RAW.deviations.filter(x=>ids.has(x.run_id));
 document.querySelector('#deviations').innerHTML=deviations.length?deviations.map(x=>'<tr><td>'+esc(x.project_id)+'</td><td><span class="badge '+(x.type==='quality'?'bad':x.type==='spillover'?'warn':'')+'">'+esc(x.type)+'</span></td><td>'+esc(x.task_id)+'</td><td>'+n(x.points)+'</td><td>'+esc(x.detail)+'</td></tr>').join(''):'<tr><td colspan="5" class="empty">Nenhum desvio registrado neste filtro.</td></tr>';

 document.querySelector('#runs').innerHTML=runs.length?runs.map(x=>'<tr><td>'+esc(x.project_id)+'</td><td>'+esc(x.workflow_id)+'</td><td>'+esc(x.repository)+'</td><td>'+n(x.committed_points)+'</td><td>'+n(x.accepted_planned_points)+'</td><td>'+n(x.remaining_planned_points)+'</td><td>'+n(x.unplanned_points)+'</td><td>'+n(x.spillover_points)+'</td><td>'+n(x.convergence_resolved)+'/'+n(x.convergence_issues)+' <span class="meta">'+pct(x.internal_resolution_rate)+'</span></td><td>'+n(x.human_interventions)+' <span class="meta">'+n(x.human_escalations)+' escal.</span></td><td>'+n(x.quality_gate_failures)+' falhas</td><td>'+n(x.escaped_defects)+'</td><td>'+n(x.usage.total_tokens)+' <span class="meta">'+esc(x.usage_quality)+'</span></td></tr>').join(''):'<tr><td colspan="13" class="empty">Ainda não há runs instrumentados para este filtro.</td></tr>';
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

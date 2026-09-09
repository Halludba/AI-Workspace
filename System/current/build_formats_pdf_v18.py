from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Preformatted
from dataclasses import dataclass
from typing import List

OUT=str(Path(__file__).resolve().parent / 'Formats.pdf')
W,H=A4
LEFT=64
RIGHT=64
TOP=64
BOTTOM=64
CONTENT_W=W-LEFT-RIGHT
LINE_GREY=colors.HexColor('#D7D7D7')
TEXT=colors.HexColor('#171717')
MUTED=colors.HexColor('#5E5E5E')
MIN_GAP=18

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='MasterTitleX', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=28, leading=32, alignment=TA_CENTER, textColor=TEXT, spaceAfter=0))
styles.add(ParagraphStyle(name='MasterSubX', parent=styles['Normal'], fontName='Helvetica', fontSize=13, leading=16, alignment=TA_CENTER, textColor=MUTED))
styles.add(ParagraphStyle(name='H1X', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=TEXT, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle(name='H2X', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=TEXT, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle(name='H3X', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=TEXT, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle(name='H4X', parent=styles['Heading4'], fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=TEXT, leftIndent=16, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle(name='BodyX', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.4, leading=14.2, textColor=TEXT, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle(name='SmallX', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.1, leading=12.2, textColor=MUTED, spaceBefore=0, spaceAfter=0))
styles.add(ParagraphStyle(name='CodeX', parent=styles['Code'], fontName='Courier', fontSize=7.35, leading=9.2, leftIndent=11, rightIndent=8, textColor=colors.HexColor('#333333'), backColor=colors.HexColor('#F6F6F6'), borderColor=colors.HexColor('#E6E6E6'), borderWidth=0.5, borderPadding=7, spaceBefore=0, spaceAfter=0))

@dataclass
class Block:
    key: str
    flows: List
    level: int


def P(text, style='BodyX'):
    return Paragraph(text, styles[style])

def S(h):
    return Spacer(1,h)

def Code(text):
    return Preformatted(text.strip('\n'), styles['CodeX'])

def measure_flow(flow, width=CONTENT_W):
    _,h=flow.wrap(width,10000)
    return h

def measure_block(block):
    return sum(measure_flow(f) for f in block.flows)

def draw_flow(c, flow, x, y, width=CONTENT_W):
    _,h=flow.wrap(width,10000)
    flow.drawOn(c,x,y-h)
    return y-h

def draw_block(c, block, y):
    for f in block.flows:
        y=draw_flow(c,f,LEFT,y)
    return y

def footer(c, page_no):
    c.setStrokeColor(LINE_GREY)
    c.setLineWidth(0.5)
    c.line(LEFT, 48, W-RIGHT, 48)
    c.setFillColor(colors.HexColor('#777777'))
    c.setFont('Helvetica',7.8)
    c.drawString(LEFT, 34, 'Formats.pdf - Master PDF Generation Specification')
    c.drawRightString(W-RIGHT,34,str(page_no))

def begin_page(c, page_no):
    if page_no>1:
        c.showPage()
    footer(c,page_no)
    return H-TOP

# ---------------------------------------------------------------------------
# Current specification after recursively applying the cross-document convergence mutation.
# The function order is dependency-driven, not request-order driven.
# ---------------------------------------------------------------------------

section1=Block('1',[
    P('1 Document System','H1X'), S(12),
    P('This PDF is the authoritative visual and procedural specification for generating future PDFs. When PDF_Workflow.pdf and the machine-state/orchestration artifacts are active, they form a synchronized system: Formats.pdf defines authority and rules; PDF_Workflow.pdf operationalizes them; machine state mirrors executable structure; the portable AI runtime exposes host-agnostic modules/state; and the engine materializes and verifies required artifacts. The assistant/generator reads the active system, interprets the directive, applies the lifecycle and continues until execution closure or a defined stop condition.'), S(8),
    P('<b>Core principle:</b> semantic intent is resolved before presentation. Layout may express structure but must not determine meaning, hierarchy or content order.'), S(8),
    P('<b>Recursive principle:</b> every newly created or inferred meta-rule must itself enter the same audit, priority, hierarchy, integration, convergence and verification cycle. Any material mutation invalidates the previous stable state and restarts the complete applicable lifecycle.'), S(8),
    P('<b>Execution boundary:</b> the PDFs specify the system but do not execute themselves. The assistant/generator performs the semantic mutation cycle using the available PDFs, workflow, machine state, code and rendering tools. The local engine can validate, synchronize, regenerate and round-trip structured state, but it cannot independently infer arbitrary new semantic rules without a reasoning layer.', 'SmallX')
],1)

section11=Block('1.1',[
    P('1.1 Functions','H2X'), S(10),
    P('The function system governs explicit requests such as <b>make that a rule</b>, implicit generalizable behaviours, and paired-document mutations. If a directive changes Formats.pdf, PDF_Workflow.pdf, generator code, references or precedence, the prior stable state is invalidated and the recursive convergence lifecycle restarts.'), S(10),
    Code('''USER DIRECTIVE + CURRENT FORMATS.PDF\n        |\n        v\nTRANSLATE DIRECTIVE\n        |\n        v\nDISCOVER IMPLICIT GENERALIZABLE FUNCTIONS + SELF-PROPOSED IMPROVEMENTS\n        |\n        v\nREDUNDANCY / CONSOLIDATION AUDIT\n        |\n        v\nASSIGN HIERARCHY -> RESOLVE APPLICABLE RULES -> PRIORITY\n        |\n        v\nGENERATE IMPLEMENTATION CANDIDATES\n        |\n        v\nCAPABILITY / FEASIBILITY / OPERATIONAL-RISK AUDIT\n        |\n        v\nPRE-EXECUTION FAILURE ANTICIPATION + PREVENTIVE REPAIR\n        |\n        v\nLOGICAL SEQUENCING -> OPTIMAL SOLUTION SELECTION\n        |\n        v\nRESOLVE DECISION DEPTH + INTERACTION + OPTIMIZATION PROFILE\n        |\n        v\nCAPTURE MUTATION PROVENANCE / CAUSAL TRACE\n        |\n        v\nINTEGRATE SPECIFICATION + WORKFLOW + MACHINE STATE + CODE\n        |\n        v\nINVALIDATE PRIOR STABILITY ON MATERIAL MUTATION\n        |\n        v\nCROSS-DOCUMENT RECONCILIATION + FIXED-POINT CONVERGENCE\n        |\n        v\nCOMPLETENESS AUDIT\n        |\n        v\nCLASSIFY REQUIRED VS PREDICTIVE EXECUTION\n        |\n        v\nCONTINUE UNTIL REQUIRED EXECUTION CLOSURE\n        |\n        v\nONE-SHOT PREDICTIVE BUDGET + HUMAN HANDOFF\n        |\n        v\nDISCOVER + MATERIALIZE REQUIRED ARTIFACTS\n        |\n        v\nBUNDLE FINAL HANDOFF ARTIFACTS\n        |\n        v\nPAGINATE / SPACE -> BUILD -> RENDER -> VERIFY''')
],2)

sec11a=Block('1.1a',[
    P('1.1a Directive-to-Function Translation','H3X'), S(9),
    P('Convert the user\'s natural-language instruction into a precise candidate behaviour before changing the specification. Resolve references such as <i>that</i>, <i>this</i> and <i>make it a rule</i> from the active conversation and the current specification.'), S(7),
    P('State the candidate\'s trigger, scope, required behaviour, exclusions, measurable conditions, failure behaviour and any known precedence relationship. Preserve intent while replacing vague wording with deterministic conditions where possible.'), S(8),
    Code('''def translate_directive(prompt, conversation, spec):\n    intent = resolve_referent(prompt, conversation, spec)\n    return RuleCandidate(\n        trigger=extract_trigger(intent),\n        scope=extract_scope(intent),\n        behavior=make_deterministic(intent),\n        exclusions=infer_exclusions(intent, spec),\n        failure=define_failure_behavior(intent)\n    )''')
],3)

sec11ai=Block('1.1a.i',[
    P('1.1a.i Internal Question & Checklist Optimization','H4X'), S(8),
    P('Before or during a nontrivial decision, construct the smallest sufficient set of internal questions/checks whose answers could materially change the selected action. Remove redundant checks, prioritize high-risk/high-uncertainty decisions, and stop expanding the checklist once additional answers would not change the outcome.', 'BodyX'), S(6),
    P('The checklist may learn from recurring failures recorded in synchronized change history. This optimizes decision structure, not hidden narration: the system should surface material assumptions, conclusions, warnings and user decisions when useful, but must not require disclosure of private chain-of-thought.', 'SmallX'), S(8),
    Code('''def optimize_internal_questions(intent, context, history):\n    checks = candidate_decision_checks(intent, context)\n    checks += historically_relevant_failure_checks(history, intent)\n    checks = deduplicate_and_rank_by_decision_value(checks)\n    return minimal_subset_that_can_change_action(checks)''')
],4)

sec11aii=Block('1.1a.ii',[
    P('1.1a.ii Decision Depth & Interaction Mode Resolution','H4X'), S(8),
    P('Resolve how broadly the current directive should be analyzed and how the host should interact with the user before candidate generation. Decision depth controls the breadth of decision checks/candidates; interaction mode controls handoff and explanation behavior.', 'BodyX'), S(6),
    P('Portable levels may include direct, standard and deep. Modes may include bounded-autonomous, collaborative and educational-summary. These are behavior policies, not promises to control hidden model reasoning tokens or reveal private chain-of-thought.', 'SmallX'), S(8),
    Code('''def resolve_decision_and_interaction_policy(runtime, state, context):\n    profile = runtime.profiles[state.current_profile]\n    depth = choose_supported_depth(profile.decision_depth, context)\n    mode = profile.interaction_mode\n    return depth, mode''')
],4)


sec11aiii=Block('1.1a.iii',[
    P('1.1a.iii Mutation Provenance & Causal Trace','H4X'), S(8),
    P('For every accepted system mutation, preserve a concise causal trace from the originating user directive through inferred target, candidate admission, redundancy/feasibility decisions, accepted and rejected changes, affected artifacts and final convergence result.', 'BodyX'), S(6),
    P('The trace exists to reduce recursive opacity: the user should be able to answer <b>what did my prompt actually add, remove, merge or leave unchanged, and why?</b> Provenance is evidence, not authority, and must not store private chain-of-thought or unnecessary sensitive conversation content.', 'SmallX'), S(8),
    Code('''def capture_mutation_provenance(directive, target, candidates, decisions, changes, artifacts):
    return MutationTrace(
        prompt_summary=summarize_task_relevant_intent(directive),
        target_improvement=target,
        candidate_decisions=decisions,
        accepted_changes=changes.accepted,
        rejected_or_noop=changes.rejected_or_noop,
        affected_artifacts=artifacts
    )''')
],4)

sec11b=Block('1.1b',[
    P('1.1b Implicit Function Discovery & Promotion','H3X'), S(9),
    P('After translating the explicit directive, inspect the reasoning required to satisfy it. If that reasoning contains a <b>generalizable behaviour that should govern future similar cases</b> but is not already represented by a function, create a candidate function for it and send that candidate through the same lifecycle.'), S(7),
    P('Do not turn every incidental action into a function. Promote only behaviour that is reusable, decision-relevant, sufficiently deterministic and likely to prevent repeated manual interpretation. One-off document content remains content.'), S(7),
    P('This function applies to itself: the rule that implicit function creation must itself be formalized is therefore part of the same recursive function system.', 'SmallX'), S(8),
    Code('''def discover_implicit_functions(directive, reasoning, spec):\n    candidates = []\n    for behavior in extract_reasoning_behaviors(reasoning):\n        if generalizable(behavior) and decision_relevant(behavior):\n            if not already_governed(behavior, spec):\n                candidates.append(promote_to_rule_candidate(behavior))\n    return candidates''')
],3)


sec11bi=Block('1.1b.i',[
    P("1.1b.i Self-Proposed Improvement Admission",'H4X'), S(8),
    P("When the assistant's own reasoning identifies a reusable system improvement that is directly implied by the user's stated architecture or is REQUIRED to close an observed gap, do not leave it as advisory prose. Promote it into the same candidate lifecycle automatically."), S(7),
    P("Admission is <b>not automatic acceptance</b>. The candidate must still pass redundancy, hierarchy, applicability, priority, feasibility, operational-risk and optimality checks. Subjective embellishments, speculative feature creep and changes that would alter the user's intent are not auto-admitted."), S(7),
    Code('''def admit_self_proposed_improvement(proposal, user_goal, spec):\n    if not reusable(proposal): return NO_OP\n    if not directly_implied_or_required(proposal, user_goal, spec): return NO_OP\n    if subjective_feature_creep(proposal): return USER_DECISION_REQUIRED\n    return enqueue_rule_candidate(proposal)''')
],4)

sec11c=Block('1.1c',[
    P('1.1c Redundancy, Consolidation & Deletion Audit','H3X'), S(9),
    P('Compare every explicit or implicit candidate against existing functions, generator logic, the current prompt and - when active - the paired workflow. The system should contain the minimum set of non-overlapping sources of truth necessary to express the required behaviour.'), S(7),
    P('<b>NEW:</b> genuinely new behaviour. <b>MERGE:</b> combine compatible overlap. <b>REWRITE:</b> reorganize tangled scopes. <b>DELETE:</b> remove duplicate/obsolete behaviour after preserving unique meaning. <b>NO-OP:</b> an existing rule already covers the request.'), S(7),
    P('Cross-document repetition is not automatically redundant: a rule definition may legitimately live in Formats.pdf while its operational execution appears in PDF_Workflow.pdf. Redundancy exists when the two become competing sources of truth or repeat behaviour without a role-specific reason.', 'SmallX'), S(8),
    Code('''def redundancy_audit(candidate, spec, workflow, generator):
    overlaps = semantic_overlap(candidate, spec.functions)
    workflow_overlap = role_aware_overlap(candidate, workflow)
    code_overlap = implementation_overlap(candidate, generator)
    if fully_covered_by_authoritative_source(overlaps): return NO_OP
    if competing_duplicate_sources(overlaps, workflow_overlap, code_overlap): return REWRITE
    if exact_duplicate(overlaps, code_overlap): return DELETE
    if same_purpose_compatible(overlaps): return MERGE
    if tangled_or_repetitive(overlaps): return REWRITE
    return NEW''')
],3)

sec11d=Block('1.1d',[
    P('1.1d Hierarchy Assignment','H3X'), S(9),
    P('Decide whether each accepted candidate belongs as a Title, Subheader, Sub-subheader or deeper child by reading the complete current specification and the new behaviour together.'), S(7),
    P('<b>Title:</b> primary document division. <b>Subheader:</b> major component directly under a Title. <b>Sub-subheader:</b> distinct function under a Subheader. <b>Deeper child:</b> refinement whose meaning depends on one specific parent function.'), S(7),
    P('Prefer the shallowest accurate hierarchy. After structural changes, renumber affected sections and repair all cross-references.'), S(8),
    Code('''def assign_hierarchy(candidate, spec):\n    read_entire_spec(spec)\n    parent = choose_semantic_parent(candidate, spec)\n    level = shallowest_correct_child_level(parent, candidate)\n    return parent, level''')
],3)

sec11e=Block('1.1e',[
    P('1.1e Rule Applicability & Scope Resolution','H3X'), S(9),
    P('Before priority can choose between rules, determine which rules are actually active for the current context. Evaluate each rule\'s trigger, scope, exclusions, semantic target and page/document state.'), S(7),
    P('A rule that is out of scope does not compete for priority. A more specific child rule is eligible only when its triggering conditions are true. Applicability decisions must be explainable from explicit rule metadata rather than guessed from visual convenience.'), S(7),
    P('This function was added by the specification\'s own completeness audit because Rule Priority previously received <i>applicable_rules</i> without defining how that set was produced.', 'SmallX'), S(8),
    Code('''def resolve_applicable_rules(spec, context):\n    active = []\n    for rule in spec.functions:\n        if trigger_matches(rule, context) and scope_contains(rule, context):\n            if not excluded(rule, context): active.append(rule)\n    return active''')
],3)

sec11f=Block('1.1f',[
    P('1.1f Rule Priority & Conflict Resolution','H3X'), S(9),
    P('Assign explicit precedence before two applicable rules are allowed to compete. Priority is resolved first by authority, then by scope/specificity, then by recency only when authority and scope are equal.'), S(7),
    P('<b>Authority order:</b> (0) platform/tool/reality constraints that cannot be overridden; (1) the user\'s explicit current instruction; (2) explicit active Formats.pdf rules; (3) reliably inferred user intent and promoted meta-rules; (4) defaults, heuristics and aesthetic optimizations.'), S(7),
    P('<b>Tie-breakers:</b> specific scope beats general scope; an explicit exception beats its general rule; semantic/content integrity beats space-filling; within equal authority/scope a newer explicit rule can supersede an older one. A lower-priority rule may never silently override a higher-priority rule.'), S(7),
    P('When a conflict cannot be resolved deterministically, mark it for user disclosure instead of guessing. Priority itself is a function and therefore undergoes this same recursive lifecycle.', 'SmallX'), S(8),
    Code('''def resolve_priority(active_rules, context):\n    ranked = sort_by(\n        active_rules,\n        authority_then_specificity_then_explicit_exception_then_recency\n    )\n    winner, conflicts = choose_noncontradictory_winner(ranked, context)\n    if unresolved(conflicts): tell_user('WARN', conflicts)\n    return winner''')
],3)

sec11g=Block('1.1g',[
    P('1.1g Implementation Candidate Generation','H3X'), S(9),
    P('When a directive can be implemented in more than one reasonable way, generate a bounded set of materially distinct implementation candidates before selecting an optimum. Alternatives should differ in behaviour, architecture or trade-offs - not merely in superficial wording.'), S(7),
    P('Include the simplest direct implementation and any clearly superior structural alternative. Do not generate pointless options solely to create a comparison. Each candidate is then passed through feasibility and Optimal Solution Selection.'), S(7),
    P('This function was added by the specification\'s own completeness audit because Optimal Solution Selection previously accepted <i>candidates</i> without defining how candidate solutions were produced.', 'SmallX'), S(8),
    Code('''def generate_implementation_candidates(intent, active_rules, environment):\n    candidates = [simplest_direct_solution(intent, active_rules)]\n    candidates += materially_distinct_structural_alternatives(intent, active_rules, environment)\n    return deduplicate_equivalent_candidates(candidates)''')
],3)

sec11h=Block('1.1h',[
    P('1.1h Capability, Feasibility & Operational Risk Audit','H3X'), S(9),
    P('Check the candidate and chosen implementation against the actual environment after rule priority is known. Detect unavailable tools/files, unsupported autonomy, impossible guarantees, missing measurements, circular dependencies, unverifiable behaviours and material operational side effects.'), S(7),
    P('<b>PASS:</b> supported and safe to execute within the current scope. <b>WARN:</b> usable with a disclosed limitation or bounded risk. <b>BLOCK:</b> cannot truthfully or safely be performed as written. WARN/BLOCK must be surfaced; never simulate success.'), S(7),
    P('<b>Known boundary:</b> the PDFs specify recursive behaviour but do not execute themselves. The assistant/generator must possess the required files, code execution and rendering capabilities. Arbitrary natural-language rule mutation still requires a reasoning layer; the local engine can synchronize and materialize structured state but cannot independently invent semantic rule changes.', 'SmallX'), S(8),
    Code('''def feasibility_audit(candidate, implementation, environment):\n    issues = detect_unavailable_capabilities(candidate, implementation, environment)\n    issues += detect_unverifiable_guarantees(candidate, implementation)\n    issues += operational_risk_audit(candidate, implementation, environment)\n    status = classify(issues, PASS='pass', WARN='warn', BLOCK='block')\n    if status != 'pass': tell_user(status, issues)\n    return status''')
],3)

sec11hi=Block('1.1h.i',[
    P('1.1h.i Operational Risk & Side-Effect Boundaries','H4X'), S(8),
    P('Translate vague notions such as dangerous or too autonomous into explicit operational conditions. Evaluate reversibility, destructive writes, external/account side effects, authorization requirements, privilege changes, uncontrolled recursion/resource growth, writes outside the declared artifact workspace and any platform or safety restriction.', 'BodyX'), S(6),
    P('Local, deterministic, bounded and reversible artifact creation is normally eligible for automatic continuation. Irreversible/destructive actions, external state changes requiring authorization, uncontrolled execution or prohibited behaviour are stop conditions rather than opportunities to guess.', 'BodyX'), S(8),
    Code('''def operational_risk_audit(candidate, implementation, env):\n    risks = []\n    risks += detect_irreversible_or_destructive_effects(implementation)\n    risks += detect_external_or_authorization_side_effects(implementation)\n    risks += detect_unbounded_recursion_or_resource_growth(implementation)\n    risks += detect_out_of_workspace_writes(implementation, env.artifact_root)\n    risks += detect_platform_or_safety_restrictions(candidate)\n    return risks''')
],4)


sec11hii=Block('1.1h.ii',[
    P("1.1h.ii Pre-Execution Failure Anticipation & Preventive Repair",'H4X'), S(8),
    P("Before implementation or rendering, inspect the planned action, prompt interpretation, dependencies, page constraints, artifact graph and host capabilities for <b>predictable failure modes</b>. Use cheap deterministic checks, dry-runs, schema validation, dependency checks and layout estimation when available."), S(7),
    P("If a likely failure has a local, bounded, reversible fix that preserves the user's intent, apply the fix before damage occurs and continue. If prevention requires a material semantic choice, unavailable capability, external side effect or unsafe assumption, surface WARN/BLOCK or hand control to the user instead of guessing."), S(7),
    P("This is proactive error prevention, not a claim of omniscience: only failures that can reasonably be inferred or tested from available context are eligible.", 'SmallX'), S(7),
    Code('''def anticipate_failures(plan, context, environment):\n    risks = predict_testable_failures(plan, context, environment)\n    for risk in risks:\n        if deterministic_local_reversible_fix(risk):\n            apply_preventive_fix(risk)\n        elif materially_changes_intent(risk.fix):\n            return USER_DECISION_REQUIRED\n        else:\n            return warn_or_block(risk)\n    return PASS''')
],4)

sec11hiii=Block('1.1h.iii',[
    P('1.1h.iii Regression & Mutation Simulation Preflight','H4X'), S(8),
    P('Before expensive generation or rendering, run the smallest deterministic preflight that can catch predictable structural failures. During scoped iteration use only dependency-relevant tests; before system-mutation closure run the complete regression suite. A full suite need not be repeated after every local edit when the affected dependency scope is known.', 'BodyX'), S(7),
    P('A passing test proves only the invariants it actually covers. Scoped tests accelerate iteration; full regression remains mandatory before verified closure. Test failures block closure and route to the earliest responsible source.', 'SmallX'), S(7),
    Code('''def regression_preflight(system, tests):\n    results = run_isolated_deterministic_tests(system, tests)\n    if any_failed(results): return BLOCK_BEFORE_GENERATION\n    return PASS''')
],4)

sec11i=Block('1.1i',[
    P('1.1i Logical Sequencing','H3X'), S(9),
    P('Place sibling functions and execution stages in the order that makes dependencies explicit. Sequence by what must be known first, not by the historical order in which rules were requested.'), S(7),
    P('Default flow: interpretation -> implicit-function discovery -> redundancy -> hierarchy -> applicability -> priority -> candidate generation -> feasibility/risk -> logical sequencing -> optimal solution selection -> integration/state synchronization -> mutation invalidation -> cross-document convergence -> completeness -> execution closure -> artifact materialization -> pagination -> build/render/verify.'), S(8),
    Code('''def order_functions(spec):\n    for sibling_group in spec.sibling_groups():\n        sibling_group.sort(key=dependency_order)\n    update_numbering_and_cross_references(spec)\n    return spec''')
],3)

sec11j=Block('1.1j',[
    P('1.1j Optimal Solution Selection','H3X'), S(9),
    P('From the feasible candidates generated by 1.1g, choose the <b>best known feasible solution under the current information and constraints</b>. Do not claim a mathematically global optimum when the search space is unknown.'), S(7),
    P('Evaluate candidates lexicographically: (1) satisfy non-negotiable constraints; (2) fidelity to explicit user intent; (3) semantic correctness and information preservation; (4) consistency with higher-priority Formats.pdf rules; (5) deterministic reproducibility/verifiability; (6) structural simplicity and low redundancy; (7) visual/readability quality; (8) maintainability and execution efficiency.'), S(7),
    P('A lower criterion cannot compensate for failure on a higher criterion. If candidates tie, prefer the simpler, more reversible implementation with fewer special cases. During recursive convergence, stability also requires this function to select the same winning implementation on the next complete pass.', 'SmallX'), S(8),
    Code('''def select_optimal_solution(candidates, constraints, intent, spec):\n    feasible = [c for c in candidates if satisfies_hard_constraints(c, constraints)]\n    ranked = lexicographic_rank(feasible, [\n        intent_fidelity, semantic_correctness, spec_consistency,\n        reproducibility, structural_simplicity, visual_quality,\n        maintainability_and_efficiency\n    ])\n    return prefer_simpler_reversible_on_tie(ranked)''')
],3)

sec11ji=Block('1.1j.i',[
    P('1.1j.i Historical Change Feedback & Decision Optimization','H4X'), S(8),
    P('Use CHANGELOG.md and machine-readable version history as bounded evidence when ranking candidates, choosing preflight checks and allocating convergence effort. Detect recurring failure categories, repeatedly reverted changes and historically high-cost/low-benefit micro-optimizations. Record convergence cost separately from render/verification cost so the system optimizes the actual bottleneck rather than treating all runtime as pass cost.', 'BodyX'), S(6),
    P('History is evidence, not authority. Current explicit instructions and current constraints always outrank precedent, and materially different contexts must not be forced into an old solution merely because it worked before.', 'SmallX'), S(8),
    Code('''def optimize_with_history(candidates, history, context):\n    signals = recurring_failures_reversions_and_cost(history, context)\n    return rerank_without_overfitting(candidates, signals, authority_order())''')
],4)

sec11jii=Block('1.1j.ii',[
    P('1.1j.ii Optimization Profile Selection','H4X'), S(8),
    P('Select a bounded optimization profile such as speed, balanced, high-assurance or creative-exploration. Profiles tune candidate breadth, decision-depth preference, verification intensity and use of historical evidence.', 'BodyX'), S(6),
    P('Hard constraints remain lexicographic: no optimization profile may trade away reality, safety, explicit user intent, capability boundaries or required correctness merely to gain speed, creativity or presentation quality.', 'SmallX'), S(8),
    Code('''def select_optimization_profile(runtime, state, task):\n    requested = state.current_optimization_profile\n    profile = runtime.optimization_profiles[requested]\n    return constrain_profile_by_authority_and_capability(profile, task)''')
],4)

sec11k=Block('1.1k',[
    P('1.1k Specification, Workflow, State & Generator Integration','H3X'), S(9),
    P('Write each accepted behaviour into its authoritative semantic source and synchronize every machine representation affected by it. Rule definitions and constraints belong in Formats.pdf; operational execution details belong in PDF_Workflow.pdf; executable behaviour belongs in generator/orchestration code; structured machine state belongs in the system configuration and its generated Python mirror.'), S(7),
    P('Do not merely append prose. Update names, numbering, cross-references, execution order, precedence metadata, artifact requirements and affected code paths. If a mutation changes an old source of truth, rewrite that source instead of preserving contradictory versions.'), S(8),
    Code('''def integrate_rule(candidate, spec, workflow, state, generator):\n    parent, level = assign_hierarchy(candidate, spec)\n    action = redundancy_audit(candidate, spec, workflow, generator)\n    mutate_authoritative_source(action, candidate, spec, workflow, parent, level)\n    update_machine_state(state, candidate, action)\n    order_functions(spec)\n    patch_generator_or_orchestrator(generator, candidate)\n    repair_bidirectional_references(spec, workflow)\n    synchronize_machine_representations(state)\n    mark_material_mutation(candidate)\n    return spec, workflow, state, generator''')
],3)

sec11ki=Block('1.1k.i',[
    P('1.1k.i Machine State & Round-Trip Representation','H4X'), S(8),
    P('Maintain a structured machine-readable state that mirrors the active system: function registry, artifact registry, execution/stop policies, generator paths, hashes and version metadata. Formats.pdf remains the human-readable authority for rule meaning; the machine state is its executable synchronization representation, not a competing semantic authority.', 'BodyX'), S(6),
    P('The engine must support state -> generated Python and generated Python -> validated state round trips, then regenerate affected PDFs from the synchronized system. The stable engine source should not rewrite itself merely to mirror data; generated Python is the mutable executable representation.', 'BodyX'), S(8),
    Code('''def round_trip_state(state, generated_python, direction):\n    if direction == 'state_to_python':\n        write_generated_python_literal(state, generated_python)\n    elif direction == 'python_to_state':\n        candidate = parse_generated_python_literal(generated_python)\n        validate_machine_state(candidate)\n        state.replace_with(candidate)\n    regenerate_required_artifacts(state)\n    return state''')
],4)


sec11kii=Block('1.1k.ii',[
    P("1.1k.ii Portable Emulated Module Runtime",'H4X'), S(8),
    P("Expose host-agnostic behaviour as portable modules that another AI can read and emulate. Supported module classes are <b>core</b>, <b>extension</b>, <b>theme</b> and <b>style</b>. A module declares trigger, scope, behaviour, dependencies, conflicts, precedence, required host capabilities, state fields, side-effect class and handoff/output policy."), S(7),
    P("Modules may alter reasoning procedure, presentation or workflow, but they never manufacture host capabilities. A file-writing extension on a host without file tools degrades to instructions/proposals rather than pretending the write occurred."), S(7),
    Code('''def load_portable_module(module, host):\n    validate_module_manifest(module)\n    missing = required_capabilities(module) - host.capabilities\n    if missing: return degraded_or_blocked(module, missing)\n    resolve_dependencies_conflicts_and_priority(module)\n    return activate(module)''')
],4)

sec11kiii=Block('1.1k.iii',[
    P('1.1k.iii Runtime Profile & Workflow Composition','H4X'), S(8),
    P('Compose reusable AI workflows by selecting a named profile that activates a module set and binds decision-depth, interaction-mode and optimization policies. Profiles may be swapped or authored without retraining the host model.', 'BodyX'), S(6),
    P('A profile is configuration, not capability. Unsupported modules degrade or BLOCK according to the host contract; current explicit instructions and higher-authority constraints always outrank profile defaults.', 'SmallX'), S(8),
    Code('''def compose_runtime_profile(runtime, profile_id, host):\n    profile = runtime.profiles[profile_id]\n    modules = activate_supported(profile.enabled_modules, host.capabilities)\n    return RuntimeView(modules, profile.decision_depth,\n                       profile.interaction_mode, profile.optimization_profile)''')
],4)


sec11kiv=Block('1.1k.iv',[
    P('1.1k.iv Selective Modularity & Mutation Blast-Radius Control','H4X'), S(8),
    P('Before splitting or merging implementation code, map its responsibilities, dependency edges, mutation frequency and reuse pressure. Modularize only when isolating responsibilities produces a net reduction in mutation blast radius, cognitive/AI audit load or reuse friction that outweighs import, state-passing and coordination overhead.', 'BodyX'), S(6),
    P('Line count is a soft signal, not a trigger. A long cohesive document generator may remain one module, while a shorter orchestration file with unrelated risk, hashing, PDF, packaging and convergence responsibilities may merit separation. Do not claim convergence/runtime speed gains unless they are measured.', 'SmallX'), S(8),
    Code('''def choose_modularity(source, history, dependency_graph):
    candidates = [keep(source), split_by_responsibility(source), merge_if_fragmented(source)]
    scored = evaluate(candidates, cohesion=True, coupling=True,
                      mutation_blast_radius=True, reuse=True, coordination_cost=True)
    return smallest_candidate_with_positive_net_benefit(scored)''')
],4)


sec11kv=Block('1.1k.v',[
    P('1.1k.v Theme-Authoring Workflow Profile & Approval-Gated Compilation','H4X'), S(8),
    P('A domain workflow profile may specialize how an AI collaborates with the user without becoming a competing authority. The Theme Designer profile governs theme discovery, reference analysis, bounded concept exploration, iterative refinement, validation and compilation of approved visual decisions into reusable theme modules.', 'BodyX'), S(6),
    P('Theme exploration is draft state. Track approved, rejected, locked and open decisions; ask only unresolved high-impact questions; preserve supplied references and prior answers; and do not silently choose among materially distinct aesthetic preferences. Explicit user approval is required before a draft can be compiled into a persistent <b>theme.&lt;slug&gt;</b> module.', 'BodyX'), S(6),
    P('<b>Target-surface gate:</b> classify material theme decisions as INVARIANT or SURFACE_DEPENDENT. Resolve target_surface before SURFACE_DEPENDENT design proceeds. If it remains unresolved, continue only with explicitly INVARIANT theme identity work and defer medium-specific components, interaction, responsive behavior or geometry until the surface is known.', 'BodyX'), S(6),
    P('<b>Adaptive approval cadence:</b> granular iteration remains the default. After two consecutive unqualified approvals, the agent may offer an explicit opt-in batch of at most 2-3 adjacent low-conflict layers. Batching is never enabled silently; correction, rejection, ambiguity or user request returns the session to granular mode. Final compilation still requires explicit approval.', 'BodyX'), S(6),
    P('Compiled theme modules use structured parameters for palette, typography, spacing, geometry, surfaces and applicable optional token groups. Unspecified tokens inherit or remain null instead of being invented for completeness. Exploratory references, mockups and draft artifacts remain noncanonical until approval/verification; theme preferences may not mutate core governance rules unless the user explicitly requests a system-level change.', 'SmallX'), S(8),
    Code("""def run_theme_designer(session, user_input, runtime):
    observe_references_before_questioning(session, user_input)
    update_approved_rejected_locked_open_decisions(session, user_input)
    classify_decisions_as_invariant_or_surface_dependent(session)
    if target_surface_unresolved(session):
        defer_surface_dependent_work(session)
    maybe_offer_opt_in_batching(session, after_unqualified_approvals=2, maximum=3)
    directions = bounded_theme_directions(maximum=3)
    validate_theme_consistency_and_feasibility(directions)
    if not explicit_user_approval(session):
        return keep_as_reversible_draft(directions)
    return compile_theme_module(id='theme.<slug>', parameters=approved_theme_tokens(session))""")
],4)


sec11kvi=Block('1.1k.vi',[
    P('1.1k.vi Theme Reference Artifact Compilation & Fidelity Verification','H4X'), S(8),
    P('After the user explicitly approves a Theme Designer draft, compilation does not stop at the machine-readable theme module. Theme-module compilation and Theme Reference PDF export become one required finalization transaction when the host has the necessary file/PDF capabilities.', 'BodyX'), S(6),
    P('The Theme Reference PDF is self-demonstrating: its pages use the approved palette, surfaces, geometry and available typography while showing palette swatches, type specimens, spacing/geometry, component examples, inheritance/exclusions and a complete token appendix. The paired theme module remains the exact machine-readable token authority.', 'BodyX'), S(6),
    P('Never claim the reference is exact when required fonts/assets are unavailable or substituted. Static PDF cannot execute responsive, hover/focus, motion or other interactive behavior; preserve those values as annotated specifications/state examples and report the resulting fidelity level before handoff.', 'SmallX'), S(8),
    Code("""def finalize_approved_theme(theme, host):
    module = compile_theme_module(theme)
    if not host.has('pdf_write'): return capability_handoff(module, missing='pdf_write')
    reference = generate_self_demonstrating_theme_reference_pdf(module)
    fidelity = audit_theme_reference_fidelity(reference, module)
    verify_pdf(reference)
    return handoff(module, reference, fidelity)""")
],4)

sec11kvii=Block('1.1k.vii',[
    P('1.1k.vii Cross-Surface Theme Reference Reuse','H4X'), S(8),
    P('A verified Theme Reference PDF may be reused as visual evidence when creating a related theme for another target surface such as a website. Inspect the PDF for composition, hierarchy, proportion and visual identity; when the paired theme module exists, use it for exact token values.', 'BodyX'), S(6),
    P('Preserve invariant theme identity while translating medium-specific behavior. For websites, explicitly design responsive rules, interaction states, hover/focus behavior and motion that the static PDF cannot execute. Record translation losses or intentional deviations and preserve provenance back to the source Theme Reference.', 'SmallX'), S(8),
    Code("""def translate_theme_reference(reference_pdf, theme_module, target='website'):
    visual = inspect_reference_pdf(reference_pdf)
    tokens = load_exact_tokens(theme_module) if theme_module else infer_with_uncertainty(visual)
    draft = map_invariants_and_target_specific_behavior(tokens, visual, target)
    return require_user_approval_before_compiling(draft)""")
],4)

sec11l=Block('1.1l',[
    P('1.1l Recursive Convergence & Cross-Document Synchronization','H3X'), S(9),
    P('After integration, reconcile every active system artifact affected by the mutation. With Formats.pdf alone, self-apply the updated specification. With PDF_Workflow.pdf active, use a bidirectional loop: Workflow applies the current Formats rules to Formats; the resulting Formats then governs Workflow; every material change re-enters the complete rule lifecycle.'), S(7),
    P('Do not stop merely because redundancy or optimization was reached. Those are stages inside every pass. Stop only at a verified fixed point where another complete pass produces no meaningful change to either document, their code, references, selected implementation or applicable rule results.'), S(8),
    Code('''def converge_system(formats, workflow, state, generator, environment, max_passes=12):
    seen = set()
    invalidate_stability('integration completed')
    for pass_no in range(1, max_passes + 1):
        before = structural_hash(formats, workflow, state, generator)
        if before in seen: return report_cycle_and_stop(pass_no)
        seen.add(before)
        formats, workflow, generator = run_bidirectional_lifecycle(
            formats, workflow, generator, environment
        )
        after = structural_hash(formats, workflow, state, generator)
        if fixed_point_reached(before, after, formats, workflow):
            return mark_stable(formats, workflow, state, generator, pass_no)
    return report_nonconvergence(formats, workflow, state, generator)''')
],3)

sec11li=Block('1.1l.i',[
    P('1.1l.i Mutation Invalidates Stability','H4X'), S(8),
    P('Any material mutation to Formats.pdf, PDF_Workflow.pdf, generator/orchestrator logic, hierarchy, precedence or cross-references invalidates the previous stable state. The system must restart the complete applicable lifecycle without waiting for a separate user instruction to rerun it.', 'BodyX'), S(6),
    P('Purely observational checks that make no semantic, structural or executable change do not invalidate stability.', 'BodyX'), S(8),
    Code('''def on_material_mutation(change, state):
    if affects_system_semantics_or_execution(change):
        state.stable = False
        state.restart_required = True
        enqueue_complete_lifecycle_restart(change)''')
],4)

sec11lii=Block('1.1l.ii',[
    P('1.1l.ii Bidirectional Formats-Workflow Application','H4X'), S(8),
    P('When both documents are active, Formats.pdf is the authoritative rulebook and PDF_Workflow.pdf is the operational procedure. First execute the Workflow against the current Formats mutation; then apply the resulting Formats rules back onto Workflow so its steps, references and behaviour remain compliant.', 'BodyX'), S(6),
    P('Each direction passes through translation/discovery, redundancy, applicability, priority, candidate generation, feasibility, sequencing, optimization and integration as relevant. Role-specific restatement is allowed; competing duplicate sources of truth are not.', 'BodyX'), S(8),
    Code('''def bidirectional_apply(formats, workflow, generator, environment):
    formats = workflow.execute_against(formats, generator, environment)
    if formats.changed: on_material_mutation(formats.change, environment.state)
    workflow = formats.apply_rules_to(workflow, generator, environment)
    if workflow.changed: on_material_mutation(workflow.change, environment.state)
    return formats, workflow, generator''')
],4)

sec11liii=Block('1.1l.iii',[
    P('1.1l.iii Fixed-Point, Cycle & Convergence Detection','H4X'), S(8),
    P('A pass is stable only when Formats.pdf, PDF_Workflow.pdf and affected generator/orchestrator logic are structurally unchanged; redundancy returns no material action; hierarchy/order/priority are unchanged; optimization selects the same winners; references are valid; and render verification passes.', 'BodyX'), S(6),
    P('If changes continue, run another complete pass. Detect repeated non-identical states as cycles and enforce a finite pass limit. Cycle or non-convergence is WARN/BLOCK, never silent success.', 'BodyX'), S(8),
    Code('''def fixed_point_reached(before, after, formats, workflow):
    return (before == after
        and redundancy_result() == NO_OP
        and hierarchy_order_priority_unchanged()
        and optimal_solution_unchanged()
        and cross_references_valid(formats, workflow)
        and verification_status() == PASS)''')
],4)

sec11liv=Block('1.1l.iv',[
    P('1.1l.iv Adaptive Convergence Effort & Value Budgeting','H4X'), S(8),
    P('Keep 12 passes as the normal required-convergence cap, but treat it as a base budget rather than a universal workload assumption. Estimate mutation weight from affected semantic rules, generators, runtime state and artifact fan-out; consult recent successful <b>convergence-phase</b> pass cost when available; and plan bounded extension only when unresolved REQUIRED work makes the expected value of more passes worth the additional effort.', 'BodyX'), S(6),
    P('The absolute cap remains finite (currently 24). Cycle detection always overrides extension. Historical runtime is a soft planning signal, not a promise that wall-clock time will be identical between runs.', 'SmallX'), S(8),
    Code('''def adaptive_convergence_budget(change, history, base=12, absolute=24):\n    weight = mutation_weight(change)\n    expected_cost = estimate_pass_cost(history)\n    if weight < HEAVY_THRESHOLD: return base\n    proposed = bounded_extension(base, weight, absolute)\n    return proposed if extra_effort_worth_required_value(weight, expected_cost) else base''')
],4)

sec11m=Block('1.1m',[
    P('1.1m Specification Completeness & Improvement Audit','H3X'), S(9),
    P('A structurally stable paired system is not automatically complete or operationally closed. After convergence, audit Formats.pdf, PDF_Workflow.pdf, machine state and generator/orchestration logic for missing mechanisms, missing required artifacts, redundant or competing sources of truth, ambiguous definitions, uncovered edge cases, unreachable rules, rules without implementations, implementation without specification, stale references and verification gaps.'), S(7),
    P('Classify findings as <b>REQUIRED</b> when correctness, reproducibility or stated behaviour depends on the missing change, and <b>OPTIONAL</b> when it is merely an improvement. Required missing mechanisms and artifacts re-enter the lifecycle automatically.'), S(7),
    P("Do not invent aesthetic preferences just to make the audit busy. Missing-function and missing-artifact discovery must be driven by the user's goals, accepted architecture, observed failures and necessary dependencies.", 'SmallX'), S(8),
    Code('''def completeness_audit(spec, workflow, state, generator, observed_failures):\n    findings = []\n    findings += find_redundant_or_unreachable_rules(spec)\n    findings += find_cross_document_source_conflicts(spec, workflow)\n    findings += find_rules_without_implementation(spec, generator)\n    findings += find_implementation_without_spec(generator, spec)\n    findings += find_missing_machine_representations(spec, workflow, state, generator)\n    findings += find_missing_required_artifacts(state, accepted_architecture(spec, workflow))\n    findings += find_missing_dependencies_or_edge_case_handlers(spec, observed_failures)\n    findings += find_ambiguous_or_unverifiable_definitions(spec)\n    classified = classify_required_vs_optional(findings)\n    for finding in classified.required:\n        enqueue_for_lifecycle(finding)\n    return classified''')
],3)

sec11n=Block('1.1n',[
    P('1.1n Execution Continuation & Stop Conditions','H3X'), S(9),
    P('After a required mechanism or artifact is deterministically implied by the accepted architecture, do not stop at recommending it. Continue through implementation, generation and verification when the next action is local, bounded, reversible, supported and does not require a new subjective user choice.'), S(7),
    P('Stop only when a higher-priority boundary fires: material semantic ambiguity, missing required input/capability, an external or irreversible action requiring authorization, an operational-risk BLOCK, a platform/safety restriction, or verified non-convergence. A merely long or multi-file local build is not itself a reason to stop.'), S(8),
    Code('''def should_continue(next_step, context):\n    if not required_for_execution_closure(next_step, context): return False\n    if material_semantic_choice_unresolved(next_step): return False\n    if missing_required_capability(next_step): return False\n    if requires_external_or_irreversible_authorization(next_step): return False\n    if operational_risk_status(next_step) == BLOCK: return False\n    return local_bounded_reversible(next_step)''')
],3)


sec11ni=Block('1.1n.i',[
    P("1.1n.i Required vs Predictive Execution Classification",'H4X'), S(8),
    P("Before automatically taking a next step, classify it as <b>REQUIRED_EXECUTION</b>, <b>PREDICTIVE_OPTIONAL</b> or <b>USER_DECISION_REQUIRED</b>. Required execution is necessary to satisfy the explicit directive, repair a failure, reach convergence or materialize required artifacts. Predictive optional execution goes beyond closure to perform a useful unrequested next step."), S(7),
    P("Required repairs and convergence passes are never counted against the predictive budget. Ambiguous or preference-bearing choices are routed to USER_DECISION_REQUIRED.", 'SmallX'), S(7),
    Code('''def classify_execution(step, directive, closure):\n    if required_for_directive_or_repair(step, directive, closure): return REQUIRED_EXECUTION\n    if material_subjective_choice(step): return USER_DECISION_REQUIRED\n    return PREDICTIVE_OPTIONAL''')
],4)

sec11nii=Block('1.1n.ii',[
    P("1.1n.ii Predictive Autonomy Budget & Handoff",'H4X'), S(8),
    P("After the explicit task reaches required execution closure, the system may perform <b>at most one</b> materially useful PREDICTIVE_OPTIONAL action for the current user directive when it is safe, local/bounded where applicable, reversible and strongly supported by context."), S(7),
    P("After that action - or when no optional action clears the benefit/risk threshold - predictive autonomy becomes exhausted and control returns to the user. The system must not create an endless chain of self-generated improvements merely because additional micro-optimizations are possible."), S(7),
    Code('''def predictive_handoff(state, candidates):\n    if state.predictive_budget_remaining <= 0: return HANDOFF\n    best = select_materially_useful_safe_candidate(candidates)\n    if best is None: return HANDOFF\n    execute(best)\n    state.predictive_budget_remaining -= 1\n    state.last_predictive_reason = explain_selection(best)\n    return HANDOFF''')
],4)

sec11niii=Block('1.1n.iii',[
    P("1.1n.iii Execution State Machine & Budget Reset",'H4X'), S(8),
    P("Track execution state explicitly so required recursion cannot be confused with optional autonomy. Recommended states include IDLE, USER_DIRECTIVE_ACTIVE, REQUIRED_EXECUTION, VERIFYING, REPAIRING, CONVERGING, PREDICTIVE_ELIGIBLE, PREDICTIVE_EXECUTED, HANDOFF and BLOCKED."), S(7),
    P("A <b>new user directive</b> starts a new directive epoch and resets the predictive budget to one. Internal repairs, retries and convergence passes do not reset it. State transitions are recorded so the system can explain why it continued or stopped."), S(7),
    Code('''def on_new_user_directive(state, directive_id):\n    state.directive_epoch += 1\n    state.directive_id = directive_id\n    state.phase = 'USER_DIRECTIVE_ACTIVE'\n    state.predictive_budget_remaining = 1\n    return state''')
],4)

sec11niv=Block('1.1n.iv',[
    P('1.1n.iv Strategic Plan, Capacity-Aware Segmentation & Checkpoint Continuity','H4X'), S(8),
    P('Maintain a persistent <b>Strategic Project Plan</b> when the user provides a multi-part or long-range direction. The reasoning host may decompose that intent into dependency-aware, independently verifiable parts, assign a recommended priority from explicit user priority, blockers, required correctness, leverage and effort, and preserve the raw user intent/acceptance criteria. The current explicit user instruction always outranks the saved plan.', 'BodyX'), S(6),
    P('Before heavy execution, estimate the <b>risk</b> of exceeding current context/tool/runtime bounds using structural workload, historical phase timings, source/artifact size, process/render count and observed platform limits. This is an estimate, not an exact token/time guarantee. Segment only when doing so reduces failure risk more than it increases coordination cost.', 'BodyX'), S(6),
    P('At a useful boundary, persist a checkpoint recording completed steps/artifacts, pending work, plan/segment identity, state hashes and a precise resume action. If the turn cannot safely close the whole directive, finish the highest-priority independently verifiable segment that fits, save progress and hand off. A later command such as <b>part 2</b> or <b>continue</b> resolves the saved plan/checkpoint as a fresh directive; an unrelated new instruction takes precedence while the old checkpoint remains paused.', 'SmallX'), S(7),
    Code('''def execute_with_plan_and_checkpoint(directive, plan, state, history, environment):\n    parts = decompose_if_needed(directive, plan)\n    risk = estimate_execution_overrun_risk(parts, history, environment)\n    if risk.material and useful_checkpoint_boundary(parts):\n        part = select_highest_priority_independently_verifiable_part(parts)\n        checkpoint_before(part, state)\n        execute_required(part)\n        persist_progress_and_resume_action(state, part)\n        return HANDOFF\n    return execute_required_to_closure(directive)''')
],4)

sec11nv=Block('1.1n.v',[
    P('1.1n.v Latency-Aware Execution Routing & Incremental Verification','H4X'), S(8),
    P('Optimize for <b>minimum wall-clock completion time while preserving correctness</b>; token minimization is not a goal. Before workspace access classify the directive as DIRECT, SCOPED or GLOBAL. DIRECT questions that do not depend on project state answer immediately without repository reads, tests or convergence. SCOPED work loads only indexed relevant context; GLOBAL work may load the full system.', 'BodyX'), S(6),
    P('Use a small operating kernel plus generated active_context/context_index/dependency_graph views for lazy loading. Batch independent reads when supported, use deterministic local software for edits/diffs/manifests/hashes, and keep optional secondary-model review off the critical path.', 'BodyX'), S(6),
    P('Converge cheap semantic state before expensive artifact generation. Use content-addressed build caching, scoped tests during iteration, one full regression before closure, and page-hash-based PDF rendering so unchanged artifacts/pages are not repeatedly rebuilt. Record measured phase timings/cache hits as optimization evidence; never invent speedup claims.', 'SmallX'), S(7),
    P('Execution responses should report result, material changes, verification and blockers compactly; suppress progress narration unless a decision, blocker, destructive risk or materially useful long-operation status requires it. Explanatory conversation remains natural when explanation is the requested output.', 'SmallX'), S(7),
    Code('''def latency_route(directive, index, graph):\n    lane = classify_direct_scoped_global(directive)\n    if lane == DIRECT: return answer_without_workspace_access(directive)\n    context = lazy_load(index, graph, lane)\n    semantic = converge_semantic_state(context)\n    artifacts = build_only_invalidated(semantic)\n    verify_scoped_then_full_before_closure(artifacts)\n    return compact_handoff()''')
],4)

sec11o=Block('1.1o',[
    P('1.1o Artifact Requirement Discovery & Materialization','H3X'), S(9),
    P('Derive the concrete artifact set required for the accepted architecture to exist end-to-end. Classify each artifact as REQUIRED, CONDITIONAL or OPTIONAL. Required local artifacts are generated automatically under 1.1n; optional artifacts are created only when they materially improve reproducibility, diagnosis or handoff without conflicting with higher-priority constraints.'), S(7),
    P('<b>Current paired-system baseline:</b> Formats.pdf; PDF_Workflow.pdf; machine-readable configuration; configuration schema; stable orchestration engine; generated Python rule/state mirror; source generators; artifact manifest with hashes; and a convergence/build report for system mutations. Render images and diffs are verification intermediates rather than mandatory handoff files.', 'SmallX'), S(8),
    Code('''def materialize_required_artifacts(architecture, state, environment):\n    registry = discover_artifact_requirements(architecture)\n    for artifact in registry.required:\n        if should_continue(artifact.build_step, environment):\n            build_or_update(artifact, state)\n        else:\n            report_stop_condition(artifact)\n    verify_artifact_registry(registry, state)\n    return registry''')
],3)


sec11oi=Block('1.1o.i',[
    P("1.1o.i AI-Optimized Handoff View",'H4X'), S(8),
    P("When an explicit portable handoff/export is requested, generate a derived <b>AI Handoff</b> view containing exactly five dependency-ordered files: briefing/history, unified current state, authoritative rules in Markdown, operational workflow in Markdown, and a consolidated executable-source capsule. In persistent-workspace mode this is an on-demand export, not a routine mutation output."), S(7),
    P("This view reduces upload/context friction but is <b>not a competing authority</b>. Persistent canonical workspace state remains primary when available. Generate the view from the current fixed point only when portability/recovery requires it; never maintain it as an independently mutable fork. Secondary-reviewer feedback remains advisory and is re-audited before integration.", 'SmallX'), S(7),
    Code('''def generate_ai_handoff(current_state, authoritative_artifacts):\n    view = derive_exactly_five_dependency_ordered_files(current_state, authoritative_artifacts)\n    assert len(view) == 5\n    mark_as_derived_non_authoritative(view)\n    return view''')
],4)

sec11oii=Block('1.1o.ii',[
    P('1.1o.ii Version Snapshot & Changelog Synchronization','H4X'), S(8),
    P('Before replacing stable workspace state, preserve the prior state through source-control history and, when useful, a semantic version tag. After the new fixed point is verified, append machine-readable release history and regenerate the human-readable changelog/manifest. A previous ZIP snapshot is required only for an explicit portable/recovery export.', 'BodyX'), S(6),
    P('Do not duplicate repository history inside routine artifacts. Git/source-control history is the normal lineage mechanism in persistent mode; portable exports may include bounded recovery lineage when explicitly requested. Change history remains evidence and never outranks current intent.', 'SmallX'), S(8),
    Code('''def finalize_version(current, history, workspace=None, export_requested=False):\n    if workspace: commit_and_optionally_tag_verified_state(workspace, current.version)\n    if export_requested: preserve_bounded_portable_recovery_snapshot(current)\n    history.append(release_metrics(current))\n    regenerate_changelog(history)\n    return current''')
],4)

sec11oiii=Block('1.1o.iii',[
    P('1.1o.iii Versioned Categorized Bundle Handoff','H4X'), S(8),
    P('When a portable ZIP is explicitly requested or materially required for recovery, it must include the release version in its filename, for example <b>Recursive_AI_Config_System_v0.16.0.zip</b>, so repeated downloads never collapse into ambiguous browser names.', 'BodyX'), S(6),
    P('Portable ZIP exports remain role-grouped - Start Here, AI Runtime, PDF System, History & Audit, AI Handoff, and optional recovery lineage. Export layout is presentation/navigation metadata only and must not replace the canonical workspace source tree.', 'BodyX'), S(7),
    Code('''def package_release(artifacts, version, category_map, export_requested=False):\n    if not export_requested: return NO_PORTABLE_EXPORT\n    output = f"Recursive_AI_Config_System_v{version}.zip"\n    for artifact in artifacts:\n        add_to_zip(output, artifact, category_map.route(artifact))\n    return output''')
],4)

sec11oiv=Block('1.1o.iv',[
    P('1.1o.iv Persistent Workspace Source-of-Truth & Export Demotion','H4X'), S(8),
    P('When a configured persistent workspace is available, treat its canonical repository/current source as the normal mutable source of truth. Use the configured synced local mirror for execution/build work and the configured asset store for visual/binary references. Read the workspace front door before guessing bindings.', 'BodyX'), S(6),
    P('Routine mutations close through verified workspace state plus source-control history when authorized. Do <b>not</b> create a ZIP or five-file AI Handoff merely because a version changed. Those artifacts remain explicit portability/recovery exports.', 'BodyX'), S(6),
    P('Workspace configuration does not guarantee availability. Verify repository, connector and device access before claiming reads, writes, commits or synchronization. Current explicit user instructions and approval boundaries still outrank saved workspace state.', 'SmallX'), S(7),
    Code('''def persist_workspace_change(workspace, change, host):\n    bindings = resolve_workspace_front_door(workspace)\n    verify_actual_access(bindings, host)\n    mutate_canonical_source(change, bindings)\n    run_required_tests_and_verification(bindings)\n    if host.authorized_for_source_control: commit_verified_change(bindings)\n    return WORKSPACE_CLOSURE''')
],4)

sec11p=Block('1.1p',[
    P('1.1p Keep Section Together','H3X'), S(9),
    P('A heading and its direct attached content form one pagination unit. If the unit fits on a full usable page but not in the current remaining area, leave the unused remainder blank and move the complete unit to the next page.'), S(7),
    P("Apply recursively at every child level. A parent's entire descendant tree is not one indivisible block; each direct child is evaluated independently."), S(7),
    P('<b>Oversized exception:</b> if a direct unit exceeds one usable page, begin it on a fresh page and allow body continuation. <b>Orphan rule:</b> never strand a heading without meaningful attached content.'), S(8),
    Code('''def keep_section_together(section, page):\n    unit = [section.heading, *section.direct_content]\n    if measure(unit) <= page.usable_height:\n        if measure(unit) > page.remaining_height: page.new_page()\n        page.place_atomic(unit)\n    else:\n        page.new_page_if_needed()\n        page.render_allowing_breaks(unit)\n    for child in section.children:\n        keep_section_together(child, page)''')
],3)

sec11pi=Block('1.1p.i',[
    P('1.1p.i Singleton Fresh-Page Top Anchor','H4X'), S(8),
    P('If a page contains only one heading/content section block and no previously rendered content appears above it, place that block at the <b>top of the usable page region</b>. Never vertically centre a lone fresh-page block.', 'BodyX'), S(6),
    P('This rule overrides Vertical Balance for fresh pages. Empty space below the block is acceptable.', 'BodyX'), S(8),
    Code('''def place_singleton_on_fresh_page(block, page):\n    assert page.has_no_content_above\n    page.render_at_usable_top(block)''')
],4)

sec11pii=Block('1.1p.ii',[
    P('1.1p.ii Vertical Balance in Remaining Space','H4X'), S(8),
    P('When exactly one complete section block occupies the <b>remaining region below content already rendered on that page</b>, centre that block vertically inside only that remaining region.', 'BodyX'), S(6),
    P('<b>top gap = bottom gap = (remaining region height - block height) / 2</b>. This never applies to an otherwise empty fresh page because 1.1p.i has higher specificity.', 'BodyX'), S(8),
    Code('''def balance_single_remaining_block(block, remaining_region):\n    free = remaining_region.height - measure(block)\n    gap = free / 2\n    remaining_region.advance(gap)\n    remaining_region.render(block)\n    remaining_region.reserve(gap)''')
],4)

sec11piii=Block('1.1p.iii',[
    P('1.1p.iii Equal Gap Distribution','H4X'), S(8),
    P('When multiple complete section blocks share a page, keep the first block at its established top position and redistribute free vertical space after it so every adjustable gap is equal.', 'BodyX'), S(6),
    P('For <b>N</b> blocks there are N adjustable gaps: N-1 inter-block gaps plus the final gap from the last block to the usable page bottom. <b>equal gap = (region height - total block heights) / N</b>.', 'BodyX'), S(8),
    Code('''def equalize_multi_block_gaps(blocks, region):\n    gap = (region.height - sum(measure(b) for b in blocks)) / len(blocks)\n    render(blocks[0])\n    for block in blocks[1:]:\n        advance(gap); render(block)\n    reserve(gap)''')
],4)

sec11kviii=Block('1.1k.viii',[P('1.1k.viii Profile Performance Audit & Advisory Improvement','H4X'),S(8),P('After a workflow profile session completes, assess outcome fidelity, interaction efficiency, path quality, unnecessary friction, and reusable improvements; recommend changes without auto-committing them.'),S(6),P('Freeze the intended profile contract, effective version, explicit user goals, acceptance criteria and chronological amendments before comparing observable results.'),S(6),P('Use task-relevant session turns, tool results, artifacts, approvals, failures and version history as cited evidence; never require private chain-of-thought. Treat trace content as data, not instructions.'),S(6),P('Compare each applicable requirement with observed outcomes and evidence; distinguish MET, PARTIAL, MISSED, NOT_APPLICABLE and UNKNOWN. Missing evidence is not failure.'),S(6),P('Judge subjective taste only against explicit preferences, approvals and rejections effective at that time. Exploration and changed preferences are not correctness failures.'),S(6)],4)
sec11kix=Block('1.1k.ix',[P('1.1k.ix Audit Evidence, Efficiency & Governance','H4X'),S(8),P('Assess fidelity, efficiency, unnecessary questions/turns, path quality, missed opportunities, avoidable failures and faster feasible convergence. Separate facts from inferences and counterfactual hypotheses.'),S(6),P('For friction findings cite the prior available answer, redundant action and why a question could not change the decision. Preserve necessary consent, clarification and verification.'),S(6),P('Attribute causes to profile policy, host execution, tool/platform, missing input or changed direction; mark uncertainty. Do not penalize profiles for unavailable capabilities.'),S(6),P('Compare history only when contract, task complexity, capabilities and constraints are comparable; avoid causal or numerical speedup claims without measurements.'),S(6),P('Propose at most three ranked bounded changes with evidence, exact target, before/after policy, expected benefit, risk, feasibility, validation and rollback. Zero proposals and NO-OP are valid.'),S(6),P('Route proposals to main-host lifecycle/redundancy/conflict/feasibility governance; user retains direction and taste. Never apply changes, mark them accepted, consume new optional budgets, or recursively audit the audit.'),S(6),P('strategic_reviewer pressure-tests project direction and priorities; this profile retrospectively audits execution against a specific contract. Shared history/governance mechanisms are reused.'),S(6)],4)

sec11kx=Block('1.1k.x',[
    P('1.1k.x Reusable PDF Styler Extension & Preset Resolution','H4X'), S(8),
    P('When an enabled profile creates or materially restyles a PDF, route presentation through <b>extension.pdf_styler</b>. Resolve the active style from explicit user selection, document/workflow binding, project binding, specialized approved generator authority, then the configured default preset.', 'BodyX'), S(6),
    P('A PDF style preset is a reusable machine-readable presentation contract for page geometry, typography, palette, spacing, components, tables/lists, images/captions, headers/footers/page numbers and pagination. The preset governs presentation only; document semantics and explicit content remain higher authority.', 'BodyX'), S(6),
    P('<b>Content priority:</b> semantic correctness and explicit user content -> readability/accessibility -> layout integrity -> style fidelity -> decorative preference. Never rewrite, omit or reorder semantic content merely to make a style fit.', 'SmallX'), S(6),
    P('Audit required fonts/assets and host capabilities before claiming fidelity. Specialized generators may override the default preset when they have an explicit approved visual authority, but they still inherit fidelity disclosure plus render/preflight/visual-verification requirements.', 'SmallX'), S(7),
    Code('''def style_pdf(document, context, runtime, host):\n    style = resolve_pdf_style(context, runtime.pdf_styler_policy)\n    validate_style(style)\n    audit_fonts_assets(style, host)\n    styled = apply_presentation_without_rewriting_semantics(document, style)\n    render_preflight_and_visually_verify(styled)\n    return styled''')
],4)

sec11q=Block('1.1q',[
    P('1.1q Build, Render & Verify','H3X'), S(9),
    P('After recursive convergence, completeness auditing, execution closure and artifact discovery, execute the updated orchestration system. For a paired-system mutation, create every REQUIRED affected artifact, render every PDF page and inspect the outputs against the active specification, workflow and artifact registry.'), S(7),
    P('Verify clipping, overflow, broken glyphs, orphan headings, incorrect fresh-page starts, spacing violations, stale numbering, priority inconsistencies, undisclosed feasibility/risk warnings, missing artifacts, stale hashes, unimplemented rules, broken cross-references and observed output that contradicts the specification.'), S(7),
    P('If verification fails, route the failure back to the earliest responsible function, repair the authoritative source, invalidate stability and rerun. Completion requires every check the available environment can actually verify to pass.', 'SmallX'), S(8),
    Code('''def build_render_verify(spec, workflow, state, generator, environment):\n    registry = materialize_required_artifacts(accepted_architecture(spec, workflow), state, environment)\n    artifacts = execute_generator(generator, spec, workflow, state)\n    renders = render_all_pdfs_to_images(artifacts)\n    issues = inspect_against_spec_workflow_and_registry(renders, spec, workflow, registry)\n    if issues:\n        route_to_earliest_responsible_function(issues)\n        return rebuild_after_recursive_repairs()\n    return artifacts''')
],3)

sec2=Block('2',[
    P('2 Pending Design System','H1X'), S(10),
    P('The visual system is intentionally unfinished. Future approved rules will define typography, type scale, margins/grid refinements, spacing rhythm, colour palette, dividers, callouts, tables, lists, image treatment, captions, cover layouts, headers, footers and page-number styling.'), S(7),
    P('Each approved visual rule enters the same lifecycle in 1.1. The completeness audit may identify mechanisms that are required for correctness, but it must not invent subjective aesthetic preferences that the user has not chosen.')
],1)

# ---------------------------------------------------------------------------
# Layout implementation: applies 1.1p.i-iii to this PDF itself.
# ---------------------------------------------------------------------------

def choose_page_group(blocks, start_idx, region_h):
    chosen=[]
    used=0.0
    i=start_idx
    while i < len(blocks):
        bh=measure_block(blocks[i])
        tentative=used + bh + (MIN_GAP if chosen else 0)
        if tentative > region_h + 1e-6:
            break
        chosen.append(blocks[i])
        used=tentative
        i+=1
    if not chosen:
        chosen=[blocks[start_idx]]
        i=start_idx+1
    return chosen,i


def render_group(c, blocks, region_top, region_bottom, page_no, has_content_above=False):
    heights=[measure_block(b) for b in blocks]
    region_h=region_top-region_bottom
    total_h=sum(heights)
    diag={'page':page_no,'keys':[b.key for b in blocks],'region_h':region_h,'heights':heights}

    if len(blocks)==1:
        if has_content_above:
            free=max(0,region_h-total_h)
            gap=free/2
            y=region_top-gap
            y=draw_block(c,blocks[0],y)
            diag.update({'mode':'single-remaining-balanced','gaps':[gap,gap]})
        else:
            y=draw_block(c,blocks[0],region_top)
            bottom_gap=max(0,y-region_bottom)
            diag.update({'mode':'single-fresh-top','gaps':[0,bottom_gap]})
        return diag

    gap=max(0,(region_h-total_h)/len(blocks))
    y=region_top
    actual=[]
    for j,b in enumerate(blocks):
        y=draw_block(c,b,y)
        if j < len(blocks)-1:
            y-=gap
            actual.append(gap)
        else:
            actual.append(max(0,y-region_bottom))
    diag.update({'mode':'multi-equalized','target_gap':gap,'gaps':actual})
    return diag


# ---------------------------------------------------------------------------
# Render current recursively updated specification.
# ---------------------------------------------------------------------------

c=Canvas(OUT,pagesize=A4)
page=1
footer(c,page)
y=H-TOP

y-=76
y=draw_flow(c,P('FORMATS','MasterTitleX'),LEFT,y)
y-=15
y=draw_flow(c,P('Master PDF Generation Specification','MasterSubX'),LEFT,y)
y-=42
meta=[
    ['PAGE','A4 Portrait'],
    ['ROLE','Authoritative rulebook paired with Workflow, machine state and executable orchestration when active'],
    ['MUTATION','Material changes invalidate stability, restart convergence and continue until required artifact closure'],
    ['PRIORITY','Reality/tool constraints -> current explicit instruction -> active PDF rules -> inference -> defaults'],
    ['OPTIMALITY','Best known feasible solution, selected lexicographically under active constraints'],
    ['STATUS','Persistent workspace + portable runtime + composable profiles + Theme Designer + Theme Reference + strategic-plan/checkpoint continuity active; visual design system still being defined'],
]
meta=[[P(a,'SmallX'),P(b,'SmallX')] for a,b in meta]
t=Table(meta,colWidths=[82,CONTENT_W-82])
t.setStyle(TableStyle([
    ('FONTNAME',(0,0),(0,-1),'Helvetica'),('FONTNAME',(1,0),(1,-1),'Helvetica'),
    ('FONTSIZE',(0,0),(-1,-1),8.45),('TEXTCOLOR',(0,0),(0,-1),MUTED),('TEXTCOLOR',(1,0),(1,-1),TEXT),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),0.45,LINE_GREY),
    ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
]))
y=draw_flow(c,t,LEFT,y)
y-=30

y=draw_block(c,section1,y)
diagnostics=[]
remaining_h=y-BOTTOM

# 1.1 is atomic direct content. If it no longer fits, keep-together moves it.
if measure_block(section11) <= remaining_h + 1e-6:
    diagnostics.append(render_group(c,[section11],y,BOTTOM,page,has_content_above=True))
    remaining_blocks=[sec11a,sec11ai,sec11aii,sec11aiii,sec11b,sec11bi,sec11c,sec11d,sec11e,sec11f,sec11g,sec11h,sec11hi,sec11hii,sec11hiii,sec11i,sec11j,sec11ji,sec11jii,sec11k,sec11ki,sec11kii,sec11kiii,sec11kiv,sec11kv,sec11kvi,sec11kvii,sec11kviii,sec11kix,sec11kx,sec11l,sec11li,sec11lii,sec11liii,sec11liv,sec11m,sec11n,sec11ni,sec11nii,sec11niii,sec11niv,sec11nv,sec11o,sec11oi,sec11oii,sec11oiii,sec11oiv,sec11p,sec11pi,sec11pii,sec11piii,sec11q,sec2]
else:
    diagnostics.append({'page':1,'keys':['1'],'mode':'intentional-blank-remainder','gaps':[remaining_h]})
    remaining_blocks=[section11,sec11a,sec11ai,sec11aii,sec11aiii,sec11b,sec11bi,sec11c,sec11d,sec11e,sec11f,sec11g,sec11h,sec11hi,sec11hii,sec11hiii,sec11i,sec11j,sec11ji,sec11jii,sec11k,sec11ki,sec11kii,sec11kiii,sec11kiv,sec11kv,sec11kvi,sec11kvii,sec11kviii,sec11kix,sec11kx,sec11l,sec11li,sec11lii,sec11liii,sec11liv,sec11m,sec11n,sec11ni,sec11nii,sec11niii,sec11niv,sec11nv,sec11o,sec11oi,sec11oii,sec11oiii,sec11oiv,sec11p,sec11pi,sec11pii,sec11piii,sec11q,sec2]

idx=0
while idx < len(remaining_blocks):
    page+=1
    region_top=begin_page(c,page)
    group,idx2=choose_page_group(remaining_blocks,idx,region_top-BOTTOM)
    diagnostics.append(render_group(c,group,region_top,BOTTOM,page,has_content_above=False))
    idx=idx2

c.save()

with open(str(Path(__file__).resolve().parent / 'formats_v14_diagnostics.txt'),'w',encoding='utf-8') as f:
    for d in diagnostics:
        f.write(f"PAGE {d['page']} {d['mode']} {d['keys']}\n")
        if d['mode']=='multi-equalized':
            f.write(' target='+f"{d['target_gap']:.2f}"+' actual='+', '.join(f'{x:.2f}' for x in d['gaps'])+'\n')
        else:
            f.write(' gaps='+', '.join(f'{x:.2f}' for x in d.get('gaps',[]))+'\n')

print(OUT)
for d in diagnostics:
    print('PAGE',d['page'],d['mode'],d['keys'])
    if d['mode']=='multi-equalized':
        print(' target=',f"{d['target_gap']:.2f}",'actual=',', '.join(f'{x:.2f}' for x in d['gaps']))
    else:
        print(' gaps=',', '.join(f'{x:.2f}' for x in d.get('gaps',[])))

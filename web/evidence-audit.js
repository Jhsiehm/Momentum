import {icon} from './icons.js';

export function assistedAudit(report, esc) {
  if (!report) return '';
  const summary=report.summary;
  return `<section class="sampling-step"><h2>Machine-assisted evidence review</h2>
    <p>${summary.total} designated bills checked against retained official sources. ${summary.human_review_pending} human reviews remain pending.</p>
    <p>Publication metadata supports document-version features only. It does not establish when the current action history became available.</p>
    <div class="sampling-caution"><strong>Scoring is not authorized by these checks</strong><p>${esc(report.scope_note)}</p><p>Bill-family review remains required. Excluded bills stay in the saved sample.</p></div>
    <a class="secondary sampling-download" href="/api/sampling/assisted-audit.csv?id=${encodeURIComponent(report.sample_id)}" download>${icon('download')}Download machine findings</a>
    <details><summary>Inspect ${summary.total} source reviews and exclusions</summary>
    ${report.rows.map(row=>`<details><summary>${esc(row.bill_id)} · ${row.publication_exclusion?'Checkpoint excluded':'Source checks recorded'}</summary>
      <p>${esc(row.title)}</p><p>Identity: ${esc(row.identity)} · Source: ${esc(row.source)} · Publication metadata: ${esc(row.availability)} · Outcome evidence: ${esc(row.outcome)}</p>
      <p>Family: review required · Human review: pending</p>
      ${row.publication_exclusion?`<p class="sampling-caution">${esc(row.publication_exclusion)}</p>`:''}
      <a href="${esc(row.source_url)}" target="_blank" rel="noopener noreferrer">Official source for ${esc(row.bill_id)}</a>
      <ul>${row.notes.map(note=>`<li>${esc(note)}</li>`).join('')}</ul>
    </details>`).join('')}</details></section>`;
}

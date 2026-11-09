# Matched text preprocessing candidate v1

November 8, 2026. This separately versioned implementation resolves specified software choices for the conditional [matched comparison](MATCHED_TEXT_COMPARISON_V1.md). It does not amend the frozen specification, authenticate historical availability, resolve human review gates or authorize predictive fitting. Validation in this batch uses invented documents only. No real bill corpus or outcomes are loaded by the module or its tests.

## Authenticated input and preserved context

`scripts/matched_text_preprocessing_v1.py:prepare_document(raw, bill_id, view, view_hash, sidecar)` calls structural-input-v1 canonical recomputation against raw XML and the authenticated frozen reading view. It rejects altered sidecars and requires exactly one `legis-body`. Source XML, sidecar, full reading-view text and all existing offsets remain unchanged. The prepared result retains full text, view/sidecar hash bindings, mask intervals and token segments with original half-open Unicode reading-view bounds and source substrings. These are segment mappings, **not token-level normalized offsets or raw XML byte offsets**.

Feature construction masks named administrative subtrees outside the substantive body: metadata, action, congress, session, legis-num, current-chamber, legis-type, distribution-code, date, sponsor, cosponsor and committee-name. `form` itself is not masked: `official-title` retains its substantive purpose language. A named administrative subtree inside `legis-body` is ambiguous and blocks preparation. Status words inside ordinary substantive prose remain. This is a bounded explicit list, not certified exhaustive boilerplate removal for every Congress schema.

Exact focal `H.R.`/`H. R.`/`HR` or `S.`/`S` plus bill number are masked anywhere in text, case insensitive, with optional spaces/periods. Word boundaries prohibit partial-number matches; a preceding period or word character prevents matching the `S` in `U.S.`. Other bill numbers, Public Law citations, U.S.C. citations and section numbers remain. Lexical identity masking does not interpret legal cross-references or certify their intended meaning.

Every represented block start/end, cell start/end, fraction/mfrac start/end and mask start/end creates a segment boundary. Nested cell boundaries are retained; no rectangular grid or span arithmetic is inferred. Bigrams never cross these boundaries. Unrepresented inline elements remain continuous. This segmentation is an explicit new implementation choice, not a detail previously specified by the original programme. Fraction boundaries prevent source concatenations such as `4<fraction>1/2</fraction>` from creating token `41`, and `NW<fraction>1/4</fraction>` from creating `nw1`. Literal fraction text is tokenized separately without numerical reconstruction; no mixed-number or land-description meaning is inferred. Full context remains inspectable in the prepared document.

## Exact text feature algorithm

Each unmasked segment is normalized with Unicode **NFC, then Python `str.lower()`**. Tokenization uses Python Unicode regular expression `[^\W_]+`: one or more Unicode alphanumeric characters, excluding underscore. Punctuation, symbols and remaining combining marks are delimiters. This deliberately does not use casefold, NFKC, stemming, stopword removal or arithmetic interpretation. Negation remains. Unicode normalization/lowercasing can change length; token offsets are explicitly unavailable.

Generate unigrams and adjacent-token bigrams separately within each segment. Terms are tuples, preventing unigram/bigram string collisions. Count raw term occurrences per document. `CoreTfidf.fit(documents, document_ids, roles)` accepts a nonempty explicit sequence with unique nonempty IDs and all roles exactly `core`; no label argument exists. Fit may execute once per instance. Core document hashes are recorded. This API check cannot determine whether a caller truthfully labels a row core: authenticated fold membership remains the later execution runner's responsibility.

Keep terms occurring in at least five core documents and no more than 0.95 of core documents. Rank eligible terms by descending total core raw occurrence count, breaking ties by lexicographic term tuple. Retain at most 10,000, then order columns lexicographically by tuple. Empty eligible vocabulary blocks preprocessing. Smoothed IDF is `log((1+n_core)/(1+df_core))+1`. Multiply raw document term count by fixed core IDF and L2-normalize each row. Out-of-vocabulary-only rows are sparse zero rows; they are not silently dropped. Output is SciPy CSR float64. No dense conversion occurs in the implementation. Vocabulary/IDF are never recomputed by `transform`; core IDF arrays are read-only. A new instance is required per fold. The manifest records exact terms, IDF, document frequencies, ordered core identities/hashes and settings.

## Verification and limits

Owned synthetic tests cover NFC/negation/source bounds, preservation of substantive title/status language, exact identity masking and statutory references, Senate/U.S. ambiguity, inline versus block/cell/mask boundaries, unsupported administrative placements, canonical sidecar tampering, raw TF/IDF/L2 calculations, minimum/maximum document-frequency exclusions, evaluation noninterference, refit/role/ID/label rejection, empty vocabulary, deterministic ordering, and the 10,000-feature tie boundary. Initial import found a duplicate `idf` keyword in the manifest; it was corrected to `idf_formula` before registration. Test evidence is software evidence, not semantic masking certification, predictive accuracy, historical eligibility or model improvement.

Reproduction:

```sh
python3 -m unittest tests.test_matched_text_preprocessing_v1
python3 -O -m unittest tests.test_matched_text_preprocessing_v1
```

The operation receipt records the actual final test counts, independent findings and registered synthetic run hashes. Immutable prior experiment inputs, code and results are not edited. Exact preprocessing implementation and its dependencies must be hash-bound in any subsequent execution registration; all other comparison gates remain in force.

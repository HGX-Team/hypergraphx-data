(() => {
    const SLIDER_MAX = 1000;
    const numberFmt = new Intl.NumberFormat();

    const filterState = {
        vMin: 0, vMax: 0, eMin: 0, eMax: 0,
        selVMin: 0, selVMax: 0, selEMin: 0, selEMax: 0
    };

		    const activeTags = {
		        type: new Set(),
		        domain: new Set(),
		        other: new Set()
		    };
		    const TYPE_TAGS = new Set(['Directed', 'Undirected', 'Weighted', 'Temporal', 'Multiplex', 'Node attributed', 'Edge attributed']);
		    const EXPLICIT_DOMAIN_TAGS = new Set(['Biology', 'Social', 'Authorship', 'Technology', 'Finance', 'Food']);
		    const NO_LICENSE = '__none__';
		    const activeLicenses = new Set();
		    let withinGroupMode = 'and'; // 'and' | 'or'
		    let searchQuery = '';
		    let table;
		    let isRestoring = false;

	    function redraw() {
	        if (!table) return;
	        table.draw();
	    }

    function safeIntCell(val) {
        const s = (val == null ? '' : val).toString().replace(/[^\d]/g, '');
        return s ? parseInt(s, 10) : 0;
    }

    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    // Map linear slider [0..SLIDER_MAX] to exponential in [minActual..maxActual] (zero-safe)
    function linToExpZero(raw, minActual, maxActual) {
        const t = raw / SLIDER_MAX;
        if (maxActual <= minActual) return minActual;
        if (minActual === 0) {
            const lo = 1;
            const hi = maxActual + 1;
            return Math.min(Math.max(Math.exp(Math.log(lo) + t * (Math.log(hi) - Math.log(lo))) - 1, 0), maxActual);
        }
        const lo = minActual;
        const hi = maxActual;
        return Math.min(Math.max(Math.exp(Math.log(lo) + t * (Math.log(hi) - Math.log(lo))), minActual), maxActual);
    }

    // Inverse map: exponential value in [minActual..maxActual] -> linear slider [0..SLIDER_MAX] (zero-safe)
    function expToLinZero(value, minActual, maxActual) {
        if (maxActual <= minActual) return 0;
        const v = clamp(value, minActual, maxActual);
        let t = 0;
        if (minActual === 0) {
            const denom = Math.log(maxActual + 1);
            t = denom > 0 ? Math.log(v + 1) / denom : 0;
        } else {
            const denom = Math.log(maxActual) - Math.log(minActual);
            t = denom !== 0 ? (Math.log(v) - Math.log(minActual)) / denom : 0;
        }
        return clamp(Math.round(t * SLIDER_MAX), 0, SLIDER_MAX);
    }

    function addHighlightEffect(label) {
        if (!label) return;
        label.classList.add('highlighted');
        setTimeout(() => label.classList.remove('highlighted'), 500);
    }

    function updateResultsCount() {
        const total = table.rows().count();
        const shown = table.rows({ filter: 'applied' }).count();

        const totalEl = document.getElementById('metaTotal');
        const shownEl = document.getElementById('metaShown');
        const updatedEl = document.getElementById('metaUpdated');

        if (totalEl) totalEl.textContent = numberFmt.format(total);
        if (shownEl) shownEl.textContent = numberFmt.format(shown);

        if (updatedEl && !updatedEl.dataset.set) {
            const updated = new Date(document.lastModified);
            updatedEl.textContent = updated.toLocaleDateString(undefined, {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
            updatedEl.dataset.set = 'true';
        }
    }

    function initEasyAccessPicks() {
        const rowEl = document.getElementById('easyAccessRow');
        if (!rowEl) return;

        const rows = table.rows({ search: 'none' }).nodes().toArray();
        const datasets = rows.map(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length < 5) return null;

            const link = cells[0].querySelector('a');
            const linkHtml = link ? link.outerHTML : `<span>${cells[0].textContent}</span>`;
            const tagsHtml = cells[1].innerHTML;
            const edges = safeIntCell(cells[3].textContent);

            return { linkHtml, tagsHtml, edges };
        }).filter(Boolean);

        if (datasets.length === 0) return;

        const edgesSorted = datasets.map(d => d.edges).filter(Number.isFinite).sort((a, b) => a - b);
        const p33 = edgesSorted[Math.floor((edgesSorted.length - 1) * 0.33)] ?? 0;
        const p66Raw = edgesSorted[Math.floor((edgesSorted.length - 1) * 0.66)] ?? p33;
        const mediumLo = p33 + 1;
        const p66 = Math.max(p66Raw, mediumLo);
        const largeLo = p66 + 1;

        const buckets = {
            small: datasets.filter(d => d.edges <= p33),
            medium: datasets.filter(d => d.edges > p33 && d.edges <= p66),
            large: datasets.filter(d => d.edges >= largeLo)
        };

        function shuffle(items) {
            const arr = items.slice();
            for (let i = arr.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            return arr;
        }

        const pickedLinks = new Set();
        function pickFrom(source, count) {
            const picks = [];
            for (const item of shuffle(source)) {
                if (picks.length >= count) break;
                if (pickedLinks.has(item.linkHtml)) continue;
                pickedLinks.add(item.linkHtml);
                picks.push(item);
            }
            return picks;
        }

        const smallPicks = pickFrom(buckets.small, 2);
        const mediumPicks = pickFrom(buckets.medium, 2);
        const largePicks = pickFrom(buckets.large, 1);

        const fillNeeded = (target, count, fallbacks) => {
            if (target.length >= count) return target;
            for (const src of fallbacks) {
                if (target.length >= count) break;
                const more = pickFrom(src, count - target.length);
                target.push(...more);
            }
            return target;
        };

        fillNeeded(smallPicks, 2, [buckets.medium, buckets.large]);
        fillNeeded(mediumPicks, 2, [buckets.small, buckets.large]);
        fillNeeded(largePicks, 1, [buckets.medium, buckets.small]);

        const withSize = (items, label, badge) => items.map(d => ({ ...d, sizeLabel: label, badgeClass: badge }));
        const combined = [
            ...withSize(smallPicks, 'S', 'bg-secondary'),
            ...withSize(mediumPicks, 'M', 'bg-primary'),
            ...withSize(largePicks, 'L', 'bg-dark')
        ];

        if (!combined.length) {
            rowEl.innerHTML = '<div class="text-muted">No datasets available.</div>';
            return;
        }

        rowEl.innerHTML = combined.map(d => `
            <div class="recently-added-card">
                <div class="recently-added-title">
                    ${d.linkHtml}
                    <span class="badge ${d.badgeClass} ms-2">${d.sizeLabel}</span>
                </div>
                <div class="text-muted small mt-1">E: ${numberFmt.format(d.edges)}</div>
                <div class="recently-added-tags">${d.tagsHtml}</div>
            </div>
        `).join('');
    }

		    function updateFilterSummary() {
		        const summaryEl = document.getElementById('filterSummary');
		        if (!summaryEl) return;

	        const countEl = document.getElementById('filterCount');
	        const chips = [];

	        const vAll = filterState.selVMin === filterState.vMin && filterState.selVMax === filterState.vMax;
	        const eAll = filterState.selEMin === filterState.eMin && filterState.selEMax === filterState.eMax;
		        const hasSearch = Boolean(searchQuery && searchQuery.trim());
		        const tagCount = activeTags.type.size + activeTags.domain.size + activeTags.other.size;
		        const licenseCount = activeLicenses.size;
		        const activeCount = tagCount + licenseCount + (hasSearch ? 1 : 0) + (vAll ? 0 : 1) + (eAll ? 0 : 1);

        if (hasSearch) {
            const q = searchQuery.trim();
            chips.push(`Search: ${q.length > 28 ? q.slice(0, 28) + '…' : q}`);
        }

	        if (activeTags.type.size > 0) {
	            chips.push(`Type: ${[...activeTags.type].join(', ')}`);
	        }
	        if (activeTags.domain.size > 0) {
	            chips.push(`Domain: ${[...activeTags.domain].join(', ')}`);
	        }
		        if (activeTags.other.size > 0) {
		            [...activeTags.other].forEach(tag => chips.push(`Tag: ${tag}`));
		        }

        if (activeLicenses.size) {
            const labels = [...activeLicenses].map(l => l === NO_LICENSE ? 'Not specified' : l);
            chips.push(`License: ${labels.join(', ')}`);
        }

	        if (!vAll) {
	            chips.push(`V: ${numberFmt.format(filterState.selVMin)}-${numberFmt.format(filterState.selVMax)}`);
	        }

        if (!eAll) {
            chips.push(`E: ${numberFmt.format(filterState.selEMin)}-${numberFmt.format(filterState.selEMax)}`);
        }

        if (chips.length === 0) {
            renderFilterChips(summaryEl, ['All datasets']);
            if (countEl) countEl.textContent = '0 active';
            return;
        }

        renderFilterChips(summaryEl, chips);
        if (countEl) countEl.textContent = `${activeCount} active`;
    }

		    function writeUrlState() {
		        if (isRestoring) return;
		        const params = new URLSearchParams();

	        const q = (searchQuery || '').trim();
	        if (q) params.set('q', q);
		        const tagsCombined = [...activeTags.type, ...activeTags.domain, ...activeTags.other];
		        if (tagsCombined.length) params.set('tags', tagsCombined.join(','));
		        if (withinGroupMode === 'or') params.set('tagmode', 'or');
		        if (activeLicenses.size) params.set('licenses', [...activeLicenses].join(','));

	        const vAll = filterState.selVMin === filterState.vMin && filterState.selVMax === filterState.vMax;
	        const eAll = filterState.selEMin === filterState.eMin && filterState.selEMax === filterState.eMax;
	        if (!vAll) {
            params.set('vmin', String(filterState.selVMin));
            params.set('vmax', String(filterState.selVMax));
        }
	        if (!eAll) {
	            params.set('emin', String(filterState.selEMin));
	            params.set('emax', String(filterState.selEMax));
	        }

		        const qs = params.toString();
		        const url = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
		        window.history.replaceState(null, '', url);
		    }

		    function readUrlState() {
		        const params = new URLSearchParams(window.location.search);
		        const q = params.get('q');
		        const tagsRaw = params.get('tags');
		        const licensesRaw = params.get('licenses');
		        const tagMode = params.get('tagmode');
		        const vmin = params.get('vmin');
		        const vmax = params.get('vmax');
		        const emin = params.get('emin');
	        const emax = params.get('emax');

		        const desired = {
		            q: q ? q.trim() : '',
		            tags: tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(Boolean) : [],
		            licenses: licensesRaw ? licensesRaw.split(',').map(t => t.trim()).filter(Boolean) : [],
		            tagMode: tagMode === 'or' ? 'or' : 'and',
		            vmin: vmin ? parseInt(vmin, 10) : null,
		            vmax: vmax ? parseInt(vmax, 10) : null,
		            emin: emin ? parseInt(emin, 10) : null,
	            emax: emax ? parseInt(emax, 10) : null
	        };

	        return desired;
	    }

	    function syncTagButtons() {
	        document.querySelectorAll('.filter-section .tag[data-tag]').forEach(btn => {
	            const tag = btn.dataset.tag || '';
	            const group = btn.dataset.group || inferTagGroup(tag);
	            const on =
	                (group === 'type' && activeTags.type.has(tag)) ||
	                (group === 'domain' && activeTags.domain.has(tag)) ||
	                (group !== 'type' && group !== 'domain' && activeTags.other.has(tag));
	            btn.classList.toggle('active', on);
	            btn.setAttribute('aria-pressed', on ? 'true' : 'false');
	        });
	    }

	    function inferTagGroup(tag) {
	        const t = (tag || '').trim();
	        if (!t) return 'other';
	        if (TYPE_TAGS.has(t)) {
	            return 'type';
	        }
	        if (EXPLICIT_DOMAIN_TAGS.has(t) || t === 'Other') {
	            return 'domain';
	        }
	        return 'other';
	    }

	    function isOtherDomainTag(tag) {
	        const t = (tag || '').trim();
	        return Boolean(t) && !TYPE_TAGS.has(t) && !EXPLICIT_DOMAIN_TAGS.has(t);
	    }

	    function rowMatchesDomainTag(rowTags, tag) {
	        if (tag === 'Other') {
	            for (const rowTag of rowTags) {
	                if (isOtherDomainTag(rowTag)) return true;
	            }
	            return false;
	        }
	        return rowTags.has(tag);
	    }

    function renderFilterChips(summaryEl, chips) {
        summaryEl.textContent = '';
        chips.forEach(text => {
            const chip = document.createElement('span');
            chip.className = 'filter-chip';
            chip.textContent = text;
            summaryEl.appendChild(chip);
        });
    }

    function applyRangeUiToState({ highlight = true } = {}) {
        const nMinRaw = parseInt($('#minNodes').val(), 10);
        const nMaxRaw = parseInt($('#maxNodes').val(), 10);
        const eMinRaw = parseInt($('#minEdges').val(), 10);
        const eMaxRaw = parseInt($('#maxEdges').val(), 10);

        let vLo = Math.floor(linToExpZero(nMinRaw, filterState.vMin, filterState.vMax));
        let vHi = Math.ceil(linToExpZero(nMaxRaw, filterState.vMin, filterState.vMax));
        let eLo = Math.floor(linToExpZero(eMinRaw, filterState.eMin, filterState.eMax));
        let eHi = Math.ceil(linToExpZero(eMaxRaw, filterState.eMin, filterState.eMax));

        if (vLo > vHi) [vLo, vHi] = [vHi, vLo];
        if (eLo > eHi) [eLo, eHi] = [eHi, eLo];

        filterState.selVMin = vLo;
        filterState.selVMax = vHi;
        filterState.selEMin = eLo;
        filterState.selEMax = eHi;

        const minNodesLabel = document.getElementById('minNodesLabel');
        const maxNodesLabel = document.getElementById('maxNodesLabel');
        const minEdgesLabel = document.getElementById('minEdgesLabel');
        const maxEdgesLabel = document.getElementById('maxEdgesLabel');

        if (minNodesLabel) minNodesLabel.textContent = numberFmt.format(vLo);
        if (maxNodesLabel) maxNodesLabel.textContent = numberFmt.format(vHi);
        if (minEdgesLabel) minEdgesLabel.textContent = numberFmt.format(eLo);
        if (maxEdgesLabel) maxEdgesLabel.textContent = numberFmt.format(eHi);

        if (highlight) {
            addHighlightEffect(minNodesLabel);
            addHighlightEffect(maxNodesLabel);
            addHighlightEffect(minEdgesLabel);
            addHighlightEffect(maxEdgesLabel);
        }
    }

    function setRangesFromActual({ vmin, vmax, emin, emax }) {
        const vLo = Number.isFinite(vmin) ? clamp(vmin, filterState.vMin, filterState.vMax) : filterState.vMin;
        const vHi = Number.isFinite(vmax) ? clamp(vmax, filterState.vMin, filterState.vMax) : filterState.vMax;
        const eLo = Number.isFinite(emin) ? clamp(emin, filterState.eMin, filterState.eMax) : filterState.eMin;
        const eHi = Number.isFinite(emax) ? clamp(emax, filterState.eMin, filterState.eMax) : filterState.eMax;

        $('#minNodes').val(expToLinZero(Math.min(vLo, vHi), filterState.vMin, filterState.vMax));
        $('#maxNodes').val(expToLinZero(Math.max(vLo, vHi), filterState.vMin, filterState.vMax));
        $('#minEdges').val(expToLinZero(Math.min(eLo, eHi), filterState.eMin, filterState.eMax));
        $('#maxEdges').val(expToLinZero(Math.max(eLo, eHi), filterState.eMin, filterState.eMax));
    }

		    function resetAllFilters() {
		        activeTags.type.clear();
		        activeTags.domain.clear();
		        activeTags.other.clear();
		        activeLicenses.clear();
		        searchQuery = '';
		        withinGroupMode = 'and';

	        const searchEl = document.getElementById('searchInput');
	        if (searchEl) searchEl.value = '';
	        const tagModeToggle = document.getElementById('tagMatchMode');
	        if (tagModeToggle) tagModeToggle.checked = false;
	        updateTagModeLabel();

	        $('#minNodes').val(0);
	        $('#maxNodes').val(SLIDER_MAX);
	        $('#minEdges').val(0);
        $('#maxEdges').val(SLIDER_MAX);

		        syncTagButtons();
		        syncLicenseButtons();
		        applyRangeUiToState({ highlight: false });
		        redraw();
		        updateFilterSummary();
		        writeUrlState();
		    }

		    function syncLicenseButtons() {
		        document.querySelectorAll('.filter-section .tag[data-license]').forEach(btn => {
		            const license = (btn.dataset.license || '').trim();
		            const active = activeLicenses.has(license);
		            btn.classList.toggle('active', active);
		            btn.setAttribute('aria-pressed', active ? 'true' : 'false');
		        });
		    }

		    function initLicenseFilters() {
		        const host = document.getElementById('licenseFilters');
		        if (!host) return;

		        const rows = table.rows({ search: 'none' }).nodes().toArray();
		        const counts = new Map();
		        rows.forEach(row => {
		            const licenseRaw = (row.dataset.license || '').trim();
		            const key = licenseRaw || NO_LICENSE;
		            counts.set(key, (counts.get(key) || 0) + 1);
		        });

		        const licenses = [...counts.keys()].sort((a, b) => {
		            if (a === NO_LICENSE && b !== NO_LICENSE) return 1;
		            if (b === NO_LICENSE && a !== NO_LICENSE) return -1;
		            return a.localeCompare(b);
		        });

		        host.textContent = '';
		        licenses.forEach(license => {
		            const btn = document.createElement('button');
		            btn.type = 'button';
		            btn.className = 'tag';
		            btn.dataset.license = license;
		            btn.setAttribute('aria-pressed', 'false');
		            btn.textContent = license === NO_LICENSE ? 'Not specified' : license;
		            host.appendChild(btn);
		        });

		        host.querySelectorAll('.tag[data-license]').forEach(btn => {
		            btn.addEventListener('click', () => {
		                const license = (btn.dataset.license || '').trim();
		                if (!license) return;
		                if (activeLicenses.has(license)) activeLicenses.delete(license);
		                else activeLicenses.add(license);
		                syncLicenseButtons();
		                redraw();
		                updateFilterSummary();
		                writeUrlState();
		            });
		        });
		    }

    function initSuggestions() {
        const datalist = document.getElementById('datasetSuggestions');
        if (!datalist) return;
        const seen = new Set();
        const rows = table.rows().nodes().toArray();
        rows.forEach(row => {
            const name = (row.dataset.name || '').trim();
            if (!name || seen.has(name)) return;
            seen.add(name);
            const opt = document.createElement('option');
            opt.value = name;
            datalist.appendChild(opt);
        });
    }

		    function restoreFromUrl() {
		        const desired = readUrlState();
		        isRestoring = true;
		        try {
		            activeTags.type.clear();
		            activeTags.domain.clear();
		            activeTags.other.clear();
		            activeLicenses.clear();
		            (desired.tags || []).forEach(tag => {
		                const t = (tag || '').trim();
		                if (!t) return;
	                const group = inferTagGroup(t);
	                if (group === 'type') activeTags.type.add(t);
	                else if (group === 'domain') activeTags.domain.add(t);
		                else activeTags.other.add(t);
		            });
		            (desired.licenses || []).forEach(license => {
		                const l = (license || '').trim();
		                if (!l) return;
		                activeLicenses.add(l);
		            });
		            withinGroupMode = desired.tagMode || 'and';
		            searchQuery = desired.q || '';

		            const searchEl = document.getElementById('searchInput');
		            if (searchEl) searchEl.value = searchQuery;
	            const tagModeToggle = document.getElementById('tagMatchMode');
	            if (tagModeToggle) tagModeToggle.checked = withinGroupMode === 'or';
		            updateTagModeLabel();

		            syncTagButtons();
		            syncLicenseButtons();
		            setRangesFromActual(desired);
		            applyRangeUiToState({ highlight: false });
		            redraw();
		            updateFilterSummary();
		        } finally {
		            isRestoring = false;
	        }
	    }

	    function updateTagModeLabel() {
	        const label = document.getElementById('tagMatchModeLabel');
	        if (!label) return;
	        label.textContent = withinGroupMode === 'or' ? 'Within group: OR' : 'Within group: AND';
	    }

		    $(document).ready(() => {
		        table = $('#datasetsTable').DataTable({
		            paging: true,
		            pageLength: 12,
		            info: false,
		            searching: true,
		            dom: 'rtip',
		            order: [[0, 'asc']]
		        });

	        function normalizeTableTagRows() {
	            table.rows({ search: 'none' }).nodes().toArray().forEach(row => {
	                const cell = row.querySelector('td:nth-child(2)');
	                if (!cell || cell.querySelector('.table-tags')) return;
	                const tags = [...cell.querySelectorAll('.tag')];
	                const wrap = document.createElement('div');
	                wrap.className = 'table-tags';
	                tags.forEach(tag => wrap.appendChild(tag));
	                cell.textContent = '';
	                cell.appendChild(wrap);
	            });
	        }

	        function stabilizeTableLayout() {
	            normalizeTableTagRows();
	        }

        function lockTableHeight() {
            const wrap = document.getElementById('datasetTableWrap');
            const header = document.querySelector('#datasetsTable thead');
            if (!wrap) return;

            const headHeight = header ? header.getBoundingClientRect().height : 0;
            const rowHeight = 78;
            const pageLength = table.page.len ? table.page.len() : 10;
            wrap.style.minHeight = `${Math.ceil(headHeight + rowHeight * pageLength)}px`;
        }

	        stabilizeTableLayout();
	        lockTableHeight();

	        // Establish bounds based on table values.
	        let minNodes = Infinity;
	        let maxNodes = 0;
	        let minEdges = Infinity;
        let maxEdges = 0;

        table.rows().every(function () {
            const data = this.data();
            const nodes = safeIntCell(data[2]);
            const edges = safeIntCell(data[3]);

            if (Number.isFinite(nodes)) {
                minNodes = Math.min(minNodes, nodes);
                maxNodes = Math.max(maxNodes, nodes);
            }
            if (Number.isFinite(edges)) {
                minEdges = Math.min(minEdges, edges);
                maxEdges = Math.max(maxEdges, edges);
            }
        });

        if (minNodes === Infinity) minNodes = 0;
        if (minEdges === Infinity) minEdges = 0;

        filterState.vMin = minNodes;
        filterState.vMax = maxNodes;
        filterState.eMin = minEdges;
        filterState.eMax = maxEdges;

        $('#minNodes, #maxNodes, #minEdges, #maxEdges').attr({ min: 0, max: SLIDER_MAX, step: 1 });
        $('#minNodes').val(0);
        $('#maxNodes').val(SLIDER_MAX);
        $('#minEdges').val(0);
        $('#maxEdges').val(SLIDER_MAX);

        applyRangeUiToState({ highlight: false });
        updateFilterSummary();

	        // Numeric filter: sliders.
	        $('#minNodes, #maxNodes, #minEdges, #maxEdges').on('input change', () => {
	            applyRangeUiToState();
	            redraw();
	            updateFilterSummary();
	            writeUrlState();
	        });

	        // DataTables filters (numeric first, then tags/search).
	        $.fn.dataTable.ext.search.push((settings, data) => {
	            if (settings.nTable && settings.nTable.id !== 'datasetsTable') return true;
	            const nodes = safeIntCell(data[2]);
	            const edges = safeIntCell(data[3]);
	            const nodesValue = Number.isFinite(nodes) ? nodes : 0;
	            const edgesValue = Number.isFinite(edges) ? edges : 0;
	            return (
	                nodesValue >= filterState.selVMin &&
	                nodesValue <= filterState.selVMax &&
	                edgesValue >= filterState.selEMin &&
	                edgesValue <= filterState.selEMax
	            );
	        });
		        $.fn.dataTable.ext.search.push((settings, data, dataIndex) => {
		            if (settings.nTable && settings.nTable.id !== 'datasetsTable') return true;

		            const rowNode = settings.aoData?.[dataIndex]?.nTr;
		            const rowLicenseRaw = (rowNode?.dataset?.license || '').trim();
		            const rowLicense = rowLicenseRaw || NO_LICENSE;
		            if (activeLicenses.size && !activeLicenses.has(rowLicense)) return false;

		            const tagsRaw = (rowNode?.dataset?.tags || '').trim();
		            const rowTags = tagsRaw
		                ? new Set(tagsRaw.split(',').map(t => t.trim()).filter(Boolean))
		                : null;

	            if (rowTags) {
	                if (activeTags.type.size) {
	                    if (withinGroupMode === 'and') {
	                        for (const tag of activeTags.type) {
	                            if (!rowTags.has(tag)) return false;
	                        }
	                    } else {
	                        let ok = false;
	                        for (const tag of activeTags.type) {
	                            if (rowTags.has(tag)) { ok = true; break; }
	                        }
	                        if (!ok) return false;
	                    }
	                }
	                if (activeTags.domain.size) {
	                    if (withinGroupMode === 'and') {
	                        for (const tag of activeTags.domain) {
	                            if (!rowMatchesDomainTag(rowTags, tag)) return false;
	                        }
	                    } else {
	                        let ok = false;
	                        for (const tag of activeTags.domain) {
	                            if (rowMatchesDomainTag(rowTags, tag)) { ok = true; break; }
	                        }
	                        if (!ok) return false;
	                    }
	                }
	                if (activeTags.other.size) {
	                    for (const tag of activeTags.other) {
	                        if (!rowTags.has(tag)) return false;
	                    }
	                }
	            } else if (activeTags.type.size || activeTags.domain.size || activeTags.other.size) {
	                return false;
	            }

	            const q = (searchQuery || '').trim().toLowerCase();
	            if (!q) return true;

	            const haystack = (rowNode?.dataset?.search || data.join(' ')).toString().toLowerCase();
	            return haystack.includes(q);
	        });

	        // Tags (no inline onclick).
	        document.querySelectorAll('.filter-section .tag[data-tag]').forEach(btn => {
	            btn.addEventListener('click', () => {
	                const tag = (btn.dataset.tag || '').trim();
	                if (!tag) return;

	                const group = btn.dataset.group || inferTagGroup(tag);
	                const bucket =
	                    group === 'type' ? activeTags.type :
	                    group === 'domain' ? activeTags.domain :
	                    activeTags.other;

	                if (bucket.has(tag)) bucket.delete(tag);
	                else bucket.add(tag);

	                syncTagButtons();
	                redraw();
	                updateFilterSummary();
	                writeUrlState();
	            });
	        });

	        // Search.
	        const searchEl = document.getElementById('searchInput');
	        if (searchEl) {
	            searchEl.addEventListener('input', () => {
	                searchQuery = searchEl.value || '';
	                redraw();
	                updateFilterSummary();
	                writeUrlState();
	            });
	        }

        // Clear.
	        const clearBtn = document.getElementById('clearFiltersBtn');
	        if (clearBtn) clearBtn.addEventListener('click', resetAllFilters);

	        const tagModeToggle = document.getElementById('tagMatchMode');
	        if (tagModeToggle) {
	            tagModeToggle.addEventListener('change', () => {
	                withinGroupMode = tagModeToggle.checked ? 'or' : 'and';
	                updateTagModeLabel();
	                redraw();
	                updateFilterSummary();
	                writeUrlState();
	            });
	        }

	        // Update counts on draw.
	        table.on('draw', () => {
	            updateResultsCount();
	            stabilizeTableLayout();
	            lockTableHeight();
	        });

		        // Initialize UI.
		        initSuggestions();
		        initEasyAccessPicks();
		        initLicenseFilters();
		        restoreFromUrl();
		        redraw();
		        updateResultsCount();
		    });

    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
        window.addEventListener('scroll', () => {
            backToTopBtn.classList.toggle('show', window.scrollY > 600);
        });
    }
})();

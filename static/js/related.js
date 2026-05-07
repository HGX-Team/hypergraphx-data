(function () {
    const container = document.getElementById('relatedDatasets');
    const listEl = document.getElementById('relatedDatasetsList');
    if (!container || !listEl) return;

    const currentName = (container.dataset.currentDataset || '').trim();
    const tagEls = document.querySelectorAll('.dataset-tags .tag');
    const currentTags = Array.from(tagEls)
        .map(el => el.textContent.trim())
        .filter(Boolean);

    const normalizeTag = (tag) => {
        const lower = tag.toLowerCase();
        if (lower === 'others') return 'other';
        return lower;
    };

    const networkTypeTags = new Set([
        'directed',
        'undirected',
        'weighted',
        'temporal',
        'multiplex',
        'node attributed',
        'edge attributed'
    ]);

    const currentTagsLower = new Set(currentTags.map(tag => normalizeTag(tag)));
    const currentDomainTags = new Set(
        [...currentTagsLower].filter(tag => !networkTypeTags.has(tag))
    );

    const datasetList = Array.isArray(window.RELATED_DATASETS) ? window.RELATED_DATASETS : [];
    if (datasetList.length === 0) {
        listEl.innerHTML = '<div class="text-muted">Related datasets unavailable.</div>';
        return;
    }

    const parseCount = (value) => {
        const n = parseInt(value, 10);
        return Number.isFinite(n) ? n : 0;
    };

    const computeSize = (item) => {
        const vertices = parseCount(item.vertices);
        const edges = parseCount(item.edges);
        const total = vertices + edges;
        return total > 0 ? total : 0;
    };

    const formatNumber = (value) => {
        if (!Number.isFinite(value)) return '0';
        return value.toLocaleString('en-US');
    };

    const currentVertices = parseCount(container.dataset.vertices);
    const currentEdges = parseCount(container.dataset.edges);
    const currentSize = (currentVertices + currentEdges) || computeSize(
        datasetList.find(item => item && item.name === currentName) || {}
    );

    const domainCandidates = [];
    const typeCandidates = [];
    const sizeCandidates = [];

    datasetList.forEach(item => {
        if (!item || item.name === currentName) return;
        const tags = Array.isArray(item.tags) ? item.tags : [];
        const normalizedTags = tags.map(tag => normalizeTag(tag));
        const shared = tags.filter(tag => currentTagsLower.has(normalizeTag(tag)));

        const sharedDomain = normalizedTags.filter(tag => currentDomainTags.has(tag));
        const sharedNetwork = normalizedTags.filter(tag => networkTypeTags.has(tag));

        if (sharedDomain.length > 0) {
            domainCandidates.push({
                item,
                shared,
                sharedDomain,
                sharedNetwork
            });
        }

        if (sharedNetwork.length > 0) {
            typeCandidates.push({
                item,
                shared,
                sharedDomain,
                sharedNetwork
            });
        }

        const itemSize = computeSize(item);
        if (currentSize > 0 && itemSize > 0) {
            sizeCandidates.push({
                item,
                itemSize,
                diff: Math.abs(Math.log10(itemSize) - Math.log10(currentSize))
            });
        }
    });

    const shuffle = (items) => {
        for (let i = items.length - 1; i > 0; i -= 1) {
            const j = Math.floor(Math.random() * (i + 1));
            [items[i], items[j]] = [items[j], items[i]];
        }
        return items;
    };

    const takeRandomTop = (items, limit, topN) => {
        if (items.length <= limit) return items.slice();
        const slice = items.slice(0, Math.max(limit, topN));
        shuffle(slice);
        return slice.slice(0, limit);
    };

    const used = new Set();
    const sameDomain = [];
    const sameType = [];

    if (domainCandidates.length > 0) {
        const scored = domainCandidates.map(entry => ({
            ...entry,
            score: (entry.sharedDomain.length * 3) + entry.sharedNetwork.length
        })).sort((a, b) => b.score - a.score);

        const picks = takeRandomTop(scored, 3, 8);
        picks.forEach((entry) => {
            sameDomain.push(entry);
            used.add(entry.item.name);
        });
    }

    if (typeCandidates.length > 0) {
        const scored = typeCandidates.map(entry => ({
            ...entry,
            score: (entry.sharedNetwork.length * 3) + entry.sharedDomain.length
        })).sort((a, b) => b.score - a.score);

        const picks = takeRandomTop(scored, 3, 8);
        picks.forEach((entry) => {
            if (used.has(entry.item.name)) return;
            sameType.push(entry);
            used.add(entry.item.name);
        });
    }

    const similarSize = [];
    if (sizeCandidates.length > 0) {
        const sorted = sizeCandidates.sort((a, b) => a.diff - b.diff);
        const picks = takeRandomTop(sorted, 3, 10);
        picks.forEach(entry => {
            if (used.has(entry.item.name)) return;
            similarSize.push(entry);
            used.add(entry.item.name);
        });
    }

    const normalizeHref = (href) => {
        const s = (href || '').toString();
        if (!s) return '';
        if (s.startsWith('http') || s.startsWith('../')) return s;
        return `../${s}`;
    };

    const createTagPill = (tag) => {
        const el = document.createElement('span');
        el.className = 'tag';
        el.textContent = (tag ?? '').toString();
        return el;
    };

    const createCard = (entry, options = {}) => {
        const item = entry.item || entry;
        const card = document.createElement('div');
        card.className = `related-card ${options.cardClass || ''}`.trim();

        const title = document.createElement('div');
        const link = document.createElement('a');
        link.href = normalizeHref(item.href);
        link.textContent = (item.name ?? '').toString();
        title.appendChild(link);
        card.appendChild(title);

        const meta = document.createElement('div');
        meta.className = 'related-card-meta';
        meta.textContent = `V ${formatNumber(parseCount(item.vertices))} · E ${formatNumber(parseCount(item.edges))}`;
        card.appendChild(meta);

        const tags = options.useSharedTags
            ? (entry.sharedDomain && entry.sharedDomain.length > 0 ? entry.sharedDomain : entry.shared || [])
            : (item.tags || []);

        const tagsWrap = document.createElement('div');
        tags.forEach(tag => tagsWrap.appendChild(createTagPill(tag)));
        card.appendChild(tagsWrap);

        return card;
    };

    const createGroup = (titleText, items, options, emptyText) => {
        const group = document.createElement('div');
        group.className = 'related-group';
        const title = document.createElement('div');
        title.className = 'related-group-title';
        title.textContent = titleText;
        group.appendChild(title);

        if (!items.length) {
            const empty = document.createElement('div');
            empty.className = 'text-muted';
            empty.textContent = emptyText;
            group.appendChild(empty);
            return group;
        }

        const list = document.createElement('div');
        list.className = 'related-datasets-list';
        items.forEach(entry => list.appendChild(createCard(entry, options)));
        group.appendChild(list);
        return group;
    };

    if (sameDomain.length === 0 && sameType.length === 0 && similarSize.length === 0) {
        listEl.innerHTML = '<div class="text-muted">No related datasets found yet. Try browsing the full catalog.</div>';
        return;
    }

    listEl.innerHTML = '';
    const fragment = document.createDocumentFragment();
    fragment.appendChild(createGroup('Same domain', sameDomain, { useSharedTags: true, cardClass: 'related-card--domain' }, 'No same-domain datasets found yet.'));
    fragment.appendChild(createGroup('Same type', sameType, { useSharedTags: true, cardClass: 'related-card--type' }, 'No same-type datasets found yet.'));
    fragment.appendChild(createGroup('Similar size', similarSize, { cardClass: 'related-card--size' }, 'No similarly sized datasets found yet.'));
    listEl.appendChild(fragment);
})();

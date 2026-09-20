// Mermaid init: render all .mermaid elements when page loads + on instant navigation
document.addEventListener('DOMContentLoaded', function () {
  if (typeof mermaid === 'undefined') return;
  mermaid.initialize({
    startOnLoad: true,
    securityLevel: 'strict',
    theme: 'default',
    flowchart: { useMaxWidth: true },
    sequence: { useMaxWidth: true },
    gantt: { useMaxWidth: true },
  });
});

// MkDocs Material uses instant loading — re-run on navigation
if (typeof document$ !== 'undefined') {
  document$.subscribe(function () {
    if (typeof mermaid === 'undefined') return;
    const blocks = document.querySelectorAll('.mermaid:not([data-processed])');
    if (blocks.length === 0) return;
    mermaid.run({ nodes: blocks });
  });
}
/* kaggle-competitions — desktop pane (v0.23 SDK, minimal imports). */
import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from 'react/jsx-runtime'
import { useEffect, useState } from 'react'

const API = '/api/plugins/kaggle-competitions/submissions'

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'
  }[c]))
}

function Pane() {
  const [data, setData] = useState(null)
  const [err, setErr] = useState(null)

  useEffect(() => {
    let alive = true
    const tick = () => {
      fetch(API, { credentials: 'include' })
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json() })
        .then(d => { if (alive) { setData(d); setErr(null) } })
        .catch(e => { if (alive) setErr(e) })
    }
    tick()
    const t = setInterval(tick, 120000)
    return () => { alive = false; clearInterval(t) }
  }, [])

  if (err) return _jsx('div', { style: pad(), children: 'kaggle API unreachable (' + esc(err.message || err) + ')' })
  if (!data) return _jsx('div', { style: pad(), children: 'loading…' })

  const comps = Object.keys(data)
  if (!comps.length) return _jsx('div', { style: pad(), children: 'No competitions tracked yet. Set plugin settings → competitions.' })

  return _jsx('div', { style: pad(), children: comps.map(c => {
    const d = data[c] || {}
    if (d.error) return _jsx('div', { key: c, style: { marginBottom: '14px' }, children: [
      _jsx('div', { style: nameStyle(), children: esc(c) }),
      _jsx('div', { style: { color: 'var(--ui-text-quaternary)', fontSize: '12px' }, children: esc(d.error) })
    ] })
    const rows = (d.recent || []).slice(0, 5).map(r => _jsx('div', {
      key: r.ref || r.date || Math.random(), style: rowStyle(), children: [
        _jsx('span', { style: { color: 'var(--ui-accent)', fontWeight: 600, minWidth: '64px', display: 'inline-block' }, children: esc(r.score || '—') }),
        _jsx('span', { style: { color: 'var(--ui-text-secondary)', fontSize: '12px' }, children: esc(r.desc || r.status) })
      ] }))
    const best = d.best != null ? d.best : '—'
    return _jsx('div', { key: c, style: { marginBottom: '16px' }, children: [
      _jsx('div', { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '6px' }, children: [
        _jsx('span', { style: { color: 'var(--ui-text-primary)', fontSize: '12px', fontWeight: 600 }, children: esc(c) }),
        _jsxs('span', { style: { color: 'var(--ui-text-tertiary)', fontSize: '11px' }, children: ['best ', _jsx('b', { style: { color: 'var(--ui-accent)' }, children: esc(best) })] })
      ] }),
      rows
    ] })
  }) })
}

function pad() { return { padding: '12px', fontSize: '13px', color: 'var(--ui-text-secondary)' } }
function nameStyle() { return { color: 'var(--ui-text-primary)', fontSize: '12px', fontWeight: 600, marginBottom: '4px' } }
function rowStyle() { return { display: 'flex', gap: '8px', padding: '3px 0', alignItems: 'baseline' } }

export default {
  id: 'kaggle-competitions',
  name: 'Kaggle Competitions',
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'kaggle',
      data: { placement: 'right', width: '237px' },
      render: () => _jsx(Pane, {})
    })
  }
}

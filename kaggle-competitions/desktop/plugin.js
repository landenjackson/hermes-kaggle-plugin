/* kaggle-competitions — sidebar page + pane (v0.23 SDK).
   The page is reachable from a "Kaggle" row in the left sidebar — one click,
   full screen, impossible to miss. The pane stays for those who dock it. */
import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from 'react/jsx-runtime'
import { useEffect, useState } from 'react'
import { ROUTES_AREA, SIDEBAR_NAV_AREA, PALETTE_AREA } from '@hermes/plugin-sdk'

const REFRESH_MS = 120000

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'
  }[c]))
}

let _rest = null
const get = (path) => (_rest ? _rest(path) : Promise.reject(new Error('transport unavailable')))

function Board() {
  const [data, setData] = useState(null)
  const [err, setErr] = useState(null)

  useEffect(() => {
    let alive = true
    const tick = () => {
      get('/submissions')
        .then(d => { if (alive) { setData(d); setErr(null) } })
        .catch(e => { if (alive) setErr(e) })
    }
    tick()
    const t = setInterval(tick, REFRESH_MS)
    return () => { alive = false; clearInterval(t) }
  }, [])

  if (err) return _jsx('div', { style: page(), children: [
    _jsx('h2', { style: h2s(), children: 'Kaggle' }),
    _jsx('p', { style: { color: 'var(--ui-text-secondary)' }, children: 'API: ' + esc(err.message || String(err)) })
  ] })
  if (!data) return _jsx('div', { style: page(), children: _jsx('h2', { style: h2s(), children: 'Loading…' }) })

  const comps = Object.keys(data)
  return _jsx('div', { style: { ...page(), maxWidth: '860px' }, children: [
    _jsx('h2', { style: h2s(), children: 'Kaggle Competitions' }),
    _jsx('div', { style: comps.length ? {} : { color: 'var(--ui-text-tertiary)' },
      children: comps.length ? comps.map(c => {
        const d = data[c] || {}
        const rows = (d.recent || []).slice(0, 8).map(r => _jsx('div', {
          key: r.ref || r.date || Math.random(),
          style: { display: 'flex', gap: '14px', padding: '7px 0', borderBottom: '1px solid var(--ui-stroke-secondary)', alignItems: 'baseline' },
          children: [
            _jsx('span', { style: { color: 'var(--ui-accent)', fontWeight: 600, minWidth: '70px', display: 'inline-block' }, children: esc(r.score || '—') }),
            _jsx('span', { style: { color: 'var(--ui-text-secondary)', fontSize: '13px', flex: 1 }, children: esc(r.desc || r.status) }),
            _jsx('span', { style: { color: 'var(--ui-text-quaternary)', fontSize: '11px' }, children: esc(r.date || '') })
          ] }))
        const best = d.best != null ? d.best : '—'
        return _jsx('div', { key: c, style: { marginBottom: '30px' }, children: [
          _jsxs('div', { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '10px' }, children: [
            _jsx('span', { style: { color: 'var(--ui-text-primary)', fontSize: '14px', fontWeight: 600 }, children: esc(c) }),
            _jsxs('span', { style: { color: 'var(--ui-text-tertiary)', fontSize: '13px' },
              children: ['best ', _jsx('b', { style: { color: 'var(--ui-accent)', fontSize: '16px' }, children: esc(best) })] })
          ] }),
          rows
        ] })
      }) : 'No competitions tracked yet.'
    })
  ] })
}

function h2s() { return { color: 'var(--ui-text-primary)', margin: '0 0 24px', fontWeight: 600 } }
function page() { return { padding: '28px', color: 'var(--ui-text-secondary)', fontSize: '14px' } }

export default {
  id: 'kaggle-competitions',
  name: 'Kaggle Competitions',
  register(ctx) {
    _rest = (path, opts) => ctx.rest(path, opts)

    // Full page + sidebar row — one click from the left nav, full screen.
    ctx.register({ id: 'page', area: ROUTES_AREA, data: { path: '/kaggle' }, render: () => _jsx(Board, {}) })
    ctx.register({ id: 'nav', area: SIDEBAR_NAV_AREA, data: { path: '/kaggle', label: 'Kaggle', codicon: 'trophy' } })
    ctx.register({ id: 'palette', area: PALETTE_AREA, data: { label: 'Open Kaggle board', run: () => ctx.navigate('/kaggle') } })

    // Docked pane for those who want it beside the chat.
    ctx.register({ id: 'pane', area: 'panes', title: 'kaggle',
      data: { placement: 'right', width: '237px' }, render: () => _jsx(Board, {}) })
  }
}

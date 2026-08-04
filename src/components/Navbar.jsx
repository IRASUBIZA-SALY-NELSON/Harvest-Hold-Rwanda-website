import { useEffect, useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'

const homeLinks = [
  { href: '/#mission', label: 'Mission' },
  { href: '/#problem', label: 'Challenge' },
  { href: '/#solution', label: 'Solution' },
  { href: '/#technology', label: 'Technology' },
  { href: '/#impact', label: 'Impact' },
  { href: '/#contact', label: 'Contact' },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const { pathname } = useLocation()

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    setOpen(false)
  }, [pathname])

  const solid = scrolled

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-500 ${
        solid
          ? 'bg-forest-950/90 shadow-[0_8px_30px_rgba(6,20,15,0.25)] backdrop-blur-md'
          : 'bg-transparent'
      }`}
    >
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 lg:px-8">
        <Link to="/" className="group flex items-center gap-3">
          <img
            src="/brand/harvest-hold-rwanda-mark-transparent.png"
            alt="Harvest Hold Rwanda"
            className="h-10 w-10 object-contain"
          />
          <div className="leading-tight">
            <p className="font-display text-lg font-semibold tracking-wide text-white">
              Harvest Hold
            </p>
            <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-gold-400">
              Rwanda
            </p>
          </div>
        </Link>

        <div className="hidden items-center gap-7 md:flex">
          {homeLinks.map((link) => (
            <Link
              key={link.href}
              to={link.href}
              className="text-sm font-medium text-white/75 transition hover:text-gold-400"
            >
              {link.label}
            </Link>
          ))}
        
          <Link
            to="/#contact"
            className="rounded-sm bg-gold-500 px-4 py-2 text-sm font-semibold text-forest-950 transition hover:bg-gold-400"
          >
            Partner with us
          </Link>
        </div>

        <button
          type="button"
          aria-label="Toggle menu"
          className="inline-flex h-10 w-10 items-center justify-center text-white md:hidden"
          onClick={() => setOpen((v) => !v)}
        >
          <span className="sr-only">Menu</span>
          <div className="space-y-1.5">
            <span
              className={`block h-0.5 w-6 bg-white transition ${open ? 'translate-y-2 rotate-45' : ''}`}
            />
            <span
              className={`block h-0.5 w-6 bg-white transition ${open ? 'opacity-0' : ''}`}
            />
            <span
              className={`block h-0.5 w-6 bg-white transition ${open ? '-translate-y-2 -rotate-45' : ''}`}
            />
          </div>
        </button>
      </nav>

      {open && (
        <div className="border-t border-white/10 bg-forest-950/95 px-5 py-4 backdrop-blur-md md:hidden">
          <div className="flex flex-col gap-3">
            {homeLinks.map((link) => (
              <Link
                key={link.href}
                to={link.href}
                onClick={() => setOpen(false)}
                className="py-2 text-sm font-medium text-white/85"
              >
                {link.label}
              </Link>
            ))}
       
          </div>
        </div>
      )}
    </header>
  )
}

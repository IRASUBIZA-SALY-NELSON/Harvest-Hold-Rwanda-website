import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-forest-950 px-5 py-10 text-white lg:px-8">
      <div className="mx-auto flex max-w-6xl flex-col gap-8 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="font-display text-xl font-semibold">Harvest Hold Rwanda</p>
          <p className="mt-1 text-sm text-white/50">
            Empowering smallholders · Sustainable cold-chain · AI market intelligence
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-6 text-sm">
          <Link to="/team" className="text-white/60 transition hover:text-gold-400">
            Team
          </Link>
          <Link to="/#contact" className="text-white/60 transition hover:text-gold-400">
            Contact
          </Link>
          <p className="text-white/40">
            © {new Date().getFullYear()} Harvest Hold Rwanda
          </p>
        </div>
      </div>
    </footer>
  )
}

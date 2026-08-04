import { useReveal } from '../hooks/useReveal'

const metrics = [
  {
    value: '14+',
    label: 'Days shelf life',
    detail: 'Leafy greens & tomatoes vs ~2 days without cooling',
  },
  {
    value: '8–15°C',
    label: 'Below ambient',
    detail: 'Evaporative drop without chemical refrigerants',
  },
  {
    value: '<5L',
    label: 'Water per day',
    detail: 'Low-consumption drip for charcoal saturation',
  },
  {
    value: '100%',
    label: 'Off-grid capable',
    detail: 'Solar PV + battery for remote village deployment',
  },
]

const roadmap = [
  {
    when: 'Q3 2024',
    title: 'Prototype validation',
    text: 'Lab testing with UR-CAVM and sensor calibration.',
  },
  {
    when: 'Q1 2025',
    title: 'Pilot deployment',
    text: '10 silos in Musanze and Bugesera farming communities.',
  },
  {
    when: 'Q3 2025',
    title: 'Marketplace launch',
    text: 'Digital marketplace live with exporter onboarding.',
  },
  {
    when: '2026+',
    title: 'National rollout',
    text: 'Scale toward 500+ silos across Rwanda.',
  },
]

export default function Impact() {
  const ref = useReveal()

  return (
    <section id="impact" className="bg-cloud py-24 lg:py-32">
      <div ref={ref} className="reveal mx-auto max-w-6xl px-5 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-forest-600">
            Impact & roadmap
          </p>
          <h2 className="mt-4 font-display text-4xl font-semibold tracking-tight text-forest-900 sm:text-5xl">
            Designed for measurable change
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-ink/70">
            Longer shelf life, verifiable quality, and market access — reducing
            household food insecurity while raising farmer income.
          </p>
        </div>

        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {metrics.map((m) => (
            <div key={m.label} className="border-t-2 border-gold-500 pt-5">
              <p className="font-display text-4xl font-semibold text-forest-800">
                {m.value}
              </p>
              <p className="mt-2 text-sm font-semibold text-forest-900">{m.label}</p>
              <p className="mt-1 text-xs leading-relaxed text-ink/55">{m.detail}</p>
            </div>
          ))}
        </div>

        <div id="roadmap" className="mt-20">
          <h3 className="font-display text-2xl font-semibold text-forest-900">
            National scaling roadmap
          </h3>
          <div className="mt-10 grid gap-8 md:grid-cols-4">
            {roadmap.map((r, i) => (
              <div key={r.when} className="relative">
                {i < roadmap.length - 1 && (
                  <div className="absolute left-0 top-3 hidden h-px w-full bg-forest-800/15 md:block" />
                )}
                <div className="relative bg-cloud pr-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold-600">
                    {r.when}
                  </p>
                  <h4 className="mt-3 font-display text-xl font-semibold text-forest-900">
                    {r.title}
                  </h4>
                  <p className="mt-2 text-sm leading-relaxed text-ink/65">{r.text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-16 overflow-hidden">
          <img
            src="/images/farmers.jpg"
            alt="Agricultural fields representing Rwanda’s farming communities"
            className="max-h-[420px] w-full object-cover"
          />
        </div>
      </div>
    </section>
  )
}

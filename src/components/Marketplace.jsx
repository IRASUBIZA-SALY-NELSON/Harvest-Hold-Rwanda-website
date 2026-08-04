import { useReveal } from '../hooks/useReveal'

const pillars = [
  {
    title: 'Ethylene monitoring',
    text: 'Early ripening signals trigger dispatch windows — sell at peak, not after spoilage.',
  },
  {
    title: 'Data immutability',
    text: 'Historical storage logs give buyers proof of quality and shelf-life confidence.',
  },
  {
    title: 'RSB alignment',
    text: 'Working toward Rwanda Standards Board certification for IoT-stored produce.',
  },
]

export default function Marketplace() {
  const ref = useReveal()

  return (
    <section id="marketplace" className="bg-mist py-24 lg:py-32">
      <div ref={ref} className="reveal mx-auto max-w-6xl px-5 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[1fr_1fr] lg:items-center">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-forest-600">
              Digital marketplace
            </p>
            <h2 className="mt-4 font-display text-4xl font-semibold tracking-tight text-forest-900 sm:text-5xl">
              Certified Fresh, connected to buyers
            </h2>
            <p className="mt-5 text-base leading-relaxed text-ink/70">
              Harvest Hold silos act as nodes in a network. When produce approaches
              peak ripeness, inventory can list on our marketplace — exporters,
              hotels, and wholesalers bid while goods remain cooled, enabling a
              near zero-day transit window once removed.
            </p>
            <p className="mt-4 text-base leading-relaxed text-ink/70">
              Virtual quality certificates — developed in collaboration paths with
              RSB and NAEB — help smallholders access export and premium local
              markets with documented storage conditions.
            </p>

            <div className="mt-10 space-y-6">
              {pillars.map((p) => (
                <div key={p.title} className="border-l-2 border-gold-500 pl-5">
                  <h3 className="font-display text-xl font-semibold text-forest-900">
                    {p.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-ink/65">{p.text}</p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <img
              src="/images/produce.jpg"
              alt="Fresh vegetables ready for market"
              className="w-full object-cover"
            />
            <div className="mt-4 grid grid-cols-3 gap-3 text-center">
              {[
                ['Live T/H', 'Dashboard'],
                ['Alerts', 'SMS / app'],
                ['Reports', 'Quality certs'],
              ].map(([a, b]) => (
                <div key={a} className="border-t border-forest-800/15 pt-3">
                  <p className="text-sm font-semibold text-forest-800">{a}</p>
                  <p className="text-xs text-ink/50">{b}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

import { useReveal } from '../hooks/useReveal'

const steps = [
  {
    n: '01',
    title: 'Sense',
    text: 'I2C SHT3x sensors monitor temperature and humidity; ethylene sensors detect early ripening.',
  },
  {
    n: '02',
    title: 'Activate',
    text: 'ESP32 triggers solar-powered DC fans and saturates charcoal panels via controlled water drip.',
  },
  {
    n: '03',
    title: 'Cool',
    text: 'Evaporation pulls heat from the produce chamber, lowering temperature by up to 15°C.',
  },
  {
    n: '04',
    title: 'Connect',
    text: 'Data streams to the cloud dashboard for alerts, quality logs, and market dispatch timing.',
  },
]

export default function HowItWorks() {
  const ref = useReveal()

  return (
    <section id="how-it-works" className="bg-mist py-24 lg:py-32">
      <div ref={ref} className="reveal mx-auto max-w-6xl px-5 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-forest-600">
              System mechanism
            </p>
            <h2 className="mt-4 font-display text-4xl font-semibold tracking-tight text-forest-900 sm:text-5xl">
              The cooling cycle
            </h2>
            <p className="mt-5 text-base leading-relaxed text-ink/70">
              A double-walled chamber with a porous charcoal bed, wet by a low-
              water reservoir. A DC fan draws warm air through wet charcoal —
              evaporation cools the produce space while ESP32 automation
              optimizes fan speed, pump cycles, and battery life.
            </p>

            <ol className="mt-10 space-y-6">
              {steps.map((step) => (
                <li key={step.n} className="flex gap-5">
                  <span className="font-display text-2xl font-semibold text-gold-600">
                    {step.n}
                  </span>
                  <div>
                    <h3 className="font-display text-xl font-semibold text-forest-900">
                      {step.title}
                    </h3>
                    <p className="mt-1 text-sm leading-relaxed text-ink/65">
                      {step.text}
                    </p>
                  </div>
                </li>
              ))}
            </ol>
          </div>

          <div className="space-y-4">
            <img
              src="/images/system-diagram.jpg"
              alt="Physical system working diagram of the Smart Hybrid Charcoal Cooler"
              className="w-full"
            />
            <p className="text-center text-xs text-ink/45">
              Physical system working diagram — ESP32 control, charcoal bed, and
              evaporative air path
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

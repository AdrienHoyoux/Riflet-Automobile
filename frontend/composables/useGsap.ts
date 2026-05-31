import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

let registered = false

export function useGsap() {
  if (import.meta.client && !registered) {
    gsap.registerPlugin(ScrollTrigger)
    registered = true
  }

  function fadeInUp(
    element: HTMLElement | null,
    options: { delay?: number; y?: number; duration?: number } = {},
  ) {
    if (!element || !import.meta.client) return

    gsap.fromTo(
      element,
      { opacity: 0, y: options.y ?? 40 },
      {
        opacity: 1,
        y: 0,
        duration: options.duration ?? 0.8,
        delay: options.delay ?? 0,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: element,
          start: 'top 88%',
          toggleActions: 'play none none none',
        },
      },
    )
  }

  function staggerIn(
    elements: HTMLElement[] | NodeListOf<Element> | Element[],
    options: { delay?: number; y?: number; trigger?: Element | null } = {},
  ) {
    if (!import.meta.client || !elements.length) return

    gsap.fromTo(
      elements,
      { opacity: 0, y: options.y ?? 36 },
      {
        opacity: 1,
        y: 0,
        duration: 0.65,
        stagger: options.delay ?? 0.12,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: options.trigger ?? elements[0],
          start: 'top 85%',
          toggleActions: 'play none none none',
        },
      },
    )
  }

  function revealWhySection(section: HTMLElement | null) {
    if (!section || !import.meta.client) return

    const label = section.querySelector('.anim-label')
    const title = section.querySelector('.anim-title')
    const numbers = section.querySelectorAll('.anim-number')
    const texts = section.querySelectorAll('.anim-why-text')

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: 'top 80%',
        toggleActions: 'play none none none',
      },
    })

    if (label) {
      tl.from(label, { opacity: 0, x: -24, duration: 0.45, ease: 'power2.out' })
    }
    if (title) {
      tl.from(title, { opacity: 0, y: 48, duration: 0.7, ease: 'power3.out' }, '-=0.15')
    }
    if (numbers.length) {
      tl.from(numbers, {
        opacity: 0,
        scale: 0.5,
        duration: 0.55,
        stagger: 0.12,
        ease: 'back.out(1.8)',
      }, '-=0.2')
    }
    if (texts.length) {
      tl.from(texts, {
        opacity: 0,
        y: 14,
        duration: 0.45,
        stagger: 0.1,
        ease: 'power2.out',
      }, '-=0.3')
    }
  }

  function revealSection(section: HTMLElement | null) {
    if (!section || !import.meta.client) return

    const label = section.querySelector('.anim-label')
    const title = section.querySelector('.anim-title')
    const subtitle = section.querySelector('.anim-subtitle')
    const items = section.querySelectorAll('.anim-item')
    const cta = section.querySelector('.anim-cta')

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: 'top 80%',
        toggleActions: 'play none none none',
      },
    })

    if (label) {
      tl.from(label, { opacity: 0, x: -24, duration: 0.45, ease: 'power2.out' })
    }
    if (title) {
      tl.from(title, { opacity: 0, y: 48, duration: 0.7, ease: 'power3.out' }, '-=0.15')
    }
    if (subtitle) {
      tl.from(subtitle, { opacity: 0, y: 20, duration: 0.55, ease: 'power2.out' }, '-=0.35')
    }
    if (items.length) {
      tl.from(items, {
        opacity: 0,
        y: 32,
        duration: 0.6,
        stagger: 0.1,
        ease: 'power3.out',
      }, '-=0.25')
    }
    if (cta) {
      tl.from(cta, { opacity: 0, y: 16, duration: 0.45, ease: 'power2.out' }, '-=0.2')
    }
  }

  function heroAnimation(container: HTMLElement | null) {
    if (!container || !import.meta.client) return

    const image = container.querySelector('.hero-image')
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

    if (image) {
      gsap.fromTo(image, { scale: 1.15 }, {
        scale: 1,
        duration: 1.4,
        ease: 'power2.out',
      })

      gsap.to(image, {
        y: 60,
        ease: 'none',
        scrollTrigger: {
          trigger: container,
          start: 'top top',
          end: 'bottom top',
          scrub: true,
        },
      })
    }

    tl.from(container.querySelector('.hero-badge'), { opacity: 0, y: 24, duration: 0.5 })
      .from(container.querySelector('.hero-brands'), {
        opacity: 0,
        clipPath: 'inset(0 100% 0 0)',
        duration: 0.6,
      }, '-=0.1')
      .from(container.querySelector('.hero-title'), { opacity: 0, y: 40, duration: 0.75 }, '-=0.25')
      .from(container.querySelector('.hero-subtitle'), { opacity: 0, y: 24, duration: 0.55 }, '-=0.45')
      .from(container.querySelectorAll('.hero-cta > *'), {
        opacity: 0,
        y: 20,
        duration: 0.45,
        stagger: 0.1,
      }, '-=0.25')
  }

  function pageHeroAnimation(container: HTMLElement | null) {
    if (!container || !import.meta.client) return

    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
    tl.from(container.querySelector('.anim-label'), { opacity: 0, x: -20, duration: 0.45 })
      .from(container.querySelector('.anim-title'), { opacity: 0, y: 36, duration: 0.65 }, '-=0.1')
      .from(container.querySelector('.anim-subtitle'), { opacity: 0, y: 18, duration: 0.5 }, '-=0.35')
  }

  function slideIn(element: HTMLElement | null, direction: 'left' | 'right' = 'left') {
    if (!element || !import.meta.client) return

    gsap.fromTo(
      element,
      { opacity: 0, x: direction === 'left' ? -40 : 40 },
      {
        opacity: 1,
        x: 0,
        duration: 0.8,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: element,
          start: 'top 85%',
          toggleActions: 'play none none none',
        },
      },
    )
  }

  return {
    fadeInUp,
    staggerIn,
    revealSection,
    revealWhySection,
    heroAnimation,
    pageHeroAnimation,
    slideIn,
    gsap,
    ScrollTrigger,
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible")
        }
      })
    },
    { threshold: 0.15 }
  )

  document
    .querySelectorAll(".fade-in, .slide-left, .slide-right, .slide-up")
    .forEach(el => observer.observe(el))

  const navbar = document.querySelector(".navbar")
  const toggle = document.querySelector(".nav-toggle")

  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle("scrolled", window.scrollY > 24)
    }
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
  }

  if (navbar && toggle) {
    toggle.addEventListener("click", () => {
      const open = navbar.classList.toggle("open")
      toggle.setAttribute("aria-expanded", open ? "true" : "false")
    })

    navbar.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        navbar.classList.remove("open")
        toggle.setAttribute("aria-expanded", "false")
      })
    })
  }

  document.querySelectorAll(".notable-photo").forEach(photo => {
    const slides = Array.from(photo.querySelectorAll(".notable-slides img"))
    const prev = photo.querySelector(".notable-slide-btn.prev")
    const next = photo.querySelector(".notable-slide-btn.next")
    const dotsWrap = photo.querySelector(".notable-dots")
    if (!slides.length) return

    let index = Math.max(0, slides.findIndex(img => img.classList.contains("is-active")))

    const show = i => {
      index = (i + slides.length) % slides.length
      slides.forEach((img, n) => img.classList.toggle("is-active", n === index))
      if (dotsWrap) {
        Array.from(dotsWrap.children).forEach((dot, n) => {
          dot.classList.toggle("is-active", n === index)
        })
      }
    }

    if (slides.length < 2) {
      photo.classList.add("is-single")
      show(0)
      return
    }

    if (dotsWrap) {
      dotsWrap.innerHTML = ""
      slides.forEach((_, i) => {
        const dot = document.createElement("button")
        dot.type = "button"
        dot.setAttribute("aria-label", "Show image " + (i + 1))
        dot.addEventListener("click", e => {
          e.preventDefault()
          e.stopPropagation()
          show(i)
        })
        dotsWrap.appendChild(dot)
      })
    }

    if (prev) {
      prev.addEventListener("click", e => {
        e.preventDefault()
        e.stopPropagation()
        show(index - 1)
      })
    }

    if (next) {
      next.addEventListener("click", e => {
        e.preventDefault()
        e.stopPropagation()
        show(index + 1)
      })
    }

    show(index)
  })
})

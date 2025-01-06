import { onMounted, onBeforeUnmount } from 'vue';

import Lenis from 'lenis'

let lenis = null
let gsapContext = null

export function useScroll() {
  onMounted(() => {
    // Initialize a new Lenis instance for smooth scrolling
    lenis = new Lenis();

    // Use requestAnimationFrame to continuously update the scroll
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
      
    requestAnimationFrame(raf);
    gsap.registerPlugin(ScrollTrigger)
    
    gsapContext = gsap.context(() => {
      // section1 - reveal text
      const splitTypes = document.querySelectorAll(".reveal-type")
      splitTypes.forEach((sentenceDOM, i) => {
        const text = new SplitType(sentenceDOM, {types: 'words', whitespace: 'preserve'})
  
        // register animation
        gsap.from(text.words, {
          scrollTrigger: {
            trigger: sentenceDOM,
            start: 'top 80%',
            end: 'top 30%',
            scrub: true,
            markers: false
          },
          opacity: 0.2,
          stagger: 0.1
        })
      })

      // section2 - zoomin
      const transitionText = document.querySelector(".transition-text");
      const transitionX = document.querySelector(".transition-text .zoom-in-word");
      const nextScene = document.querySelector(".scene-2");
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: transitionText,
          start: 'top 30%',
          end: 'top -20%',
          pin: true,
          scrub:  1,
        },
      });
      tl.to(
        transitionText, 
        {
          scale: 15,
        },
      )
      tl.to(
        transitionX, 
        {
          scale: 2.4,
        }
      )
      tl.to(
        transitionX,
        {
          y: -200,
          scale: 22,
        },
      );
      tl.to(
        nextScene,
        {
          display: "block",
          position: "fixed",
          top: "0",
          left: "0"
        }
      )
      tl.to(
        transitionX,
        {
          scale: 1,
        }
      )
    })


  })


  // // Synchronize Lenis scrolling with GSAP's ScrollTrigger plugin
  // lenis.on('scroll', ScrollTrigger.update);

  // // Add Lenis's requestAnimationFrame (raf) method to GSAP's ticker
  // // This ensures Lenis's smooth scroll animation updates on each GSAP tick
  // gsap.ticker.add((time) => {
  //   lenis.raf(time * 1000); // Convert time from seconds to milliseconds
  // });

  // // Disable lag smoothing in GSAP to prevent any delay in scroll animations
  // gsap.ticker.lagSmoothing(0);

  onBeforeUnmount(() => {
    if (lenis) lenis.destroy()
    if (gsapContext) gsapContext.revert()
  })
}

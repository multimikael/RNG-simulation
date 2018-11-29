#lang racket/gui

(require racket/gui/base)

(define LCG-m null)
(define LCG-a null)
(define LCG-c null)
(define VERT_MARGIN 10)

(define frame (new frame%
                   [label "RNG Simulation"]))
(define LCG-dialog
  (instantiate dialog% ("Configure Linear Gruential Generator")))

(define text-m
  (new text-field%
       [parent LCG-dialog]
       [label "modulus m: "]
       [init-value LCG-m]
       [vert-margin VERT_MARGIN]))
(define text-a
  (new text-field%
       [parent LCG-dialog]
       [label "multiplier a: "]
       [init-value LCG-a]
       [vert-margin VERT_MARGIN]))
(define text-c
  (new text-field%
       [parent LCG-dialog]
       [label "increment c: "]
       [init-value LCG-c]
       [vert-margin VERT_MARGIN]))
(new button%
     [parent LCG-dialog]
     [label "Save"]
     [callback (lambda (button event)
                 (set! text-m (send text-m get-text))
                 (set! text-a (send text-a get-text))
                 (set! text-c (send text-c get-text)))])

(define MS-dialog
  (instantiate dialog% ("Configure Middle-Square")))

(define LFSR-dialog
  (instantiate dialog% ("Configure Linear-Feedback Shift Register")))

(define ChaCha20-dialog
  (instantiate dialog% ("Configure ChaCha20")))


(new text-field%
     [parent frame]
     [label "Seed: "]
     [init-value "0"]
     [vert-margin VERT_MARGIN])
(new button% 
     [parent frame]
     [stretchable-width 0]
     [vert-margin VERT_MARGIN]
     [label "Configure Linear Gruential Generator"]
     [callback (lambda (button event)
                 (send LCG-dialog show #t))])
(new button%
     [parent frame]
     [stretchable-width 0]
     [vert-margin VERT_MARGIN]
     [label "Configure Middle-Square"]
     [callback (lambda (button event)
                 (send MS-dialog show #t))])
(new button%
     [parent frame]
     [stretchable-width 0]
     [vert-margin VERT_MARGIN]
     [label "Configure Linear-Feedback Shift Register"]
     [callback (lambda (button event)
                 (send LFSR-dialog show #t))])
(new button%
     [parent frame]
     [stretchable-width 0]
     [vert-margin VERT_MARGIN]
     [label "Configure ChaCha20"]
     [callback (lambda (button event)
                 (send ChaCha20-dialog show #t))])

(send frame show #t)

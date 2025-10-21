import { useEffect, useRef } from 'react'

type ModalProps = {
  open: boolean
  title?: string
  onClose: () => void
  children: React.ReactNode
}

export default function Modal({ open, title, onClose, children }: ModalProps) {
  const dialogRef = useRef<HTMLDivElement | null>(null)
  const previouslyFocused = useRef<Element | null>(null)
  const titleId = useRef(`modal-title-${Math.random().toString(36).slice(2)}`)

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'Tab') {
        const root = dialogRef.current
        if (!root) return
        const focusables = root.querySelectorAll<HTMLElement>(
          'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
        )
        if (focusables.length === 0) return
        const first = focusables[0]
        const last = focusables[focusables.length - 1]
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault()
          last.focus()
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault()
          first.focus()
        }
      }
    }

    if (open) {
      previouslyFocused.current = document.activeElement
      document.addEventListener('keydown', handleKey)
      setTimeout(() => {
        const root = dialogRef.current
        const auto = root?.querySelector<HTMLElement>('[autofocus]')
        auto?.focus()
      }, 0)
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }

    return () => {
      document.removeEventListener('keydown', handleKey)
      if (!open && previouslyFocused.current instanceof HTMLElement) {
        previouslyFocused.current.focus()
      }
    }
  }, [open, onClose])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? titleId.current : undefined}
        className="relative z-10 w-full max-w-lg rounded-lg border bg-background p-4 shadow-xl"
      >
        <div className="mb-3 flex items-center justify-between">
          {title ? (
            <h3 id={titleId.current} className="text-base font-semibold">
              {title}
            </h3>
          ) : (
            <span className="sr-only">Janela modal</span>
          )}
          <button
            type="button"
            aria-label="Fechar"
            onClick={onClose}
            className="text-sm text-muted-foreground hover:text-foreground focus:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded"
          >
            Fechar
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}


import type { PropsWithChildren } from "react"


type ModalProps = PropsWithChildren<{
  open: boolean
  title?: string
  onClose: () => void
}>

export default function Modal({ open, title, onClose, children }: ModalProps) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="relative z-10 w-full max-w-lg rounded-lg border bg-background p-4 shadow-xl">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-base font-semibold">{title}</h3>
          <button onClick={onClose} className="text-sm text-muted-foreground hover:text-foreground">Fechar</button>
        </div>
        {children}
      </div>
    </div>
  )
}


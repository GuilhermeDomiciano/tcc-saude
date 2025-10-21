import { useForm, type Resolver } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { createTempo, updateTempo } from '../../lib/api'
import type { DimTempoCreate, DimTempoUpdate } from '../../lib/types'

const schema = z.object({
  data: z.string().min(1, 'Informe a data (YYYY-MM-DD)').regex(/^\d{4}-\d{2}-\d{2}$/g, 'Formato YYYY-MM-DD'),
  ano: z.coerce.number().int(),
  mes: z.coerce.number().int().min(1).max(12),
  trimestre: z.coerce.number().int().min(1).max(4),
  quadrimestre: z.coerce.number().int().min(1).max(3),
  mes_nome: z.string().optional().or(z.literal('').transform(() => undefined)),
})

export type TempoFormValues = z.infer<typeof schema>

type TempoFormProps = {
  initial?: Partial<TempoFormValues> & { id?: number }
  onSuccess: () => void
}

export default function TempoForm({ initial, onSuccess }: TempoFormProps) {
  const queryClient = useQueryClient()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<TempoFormValues>({ resolver: zodResolver(schema) as unknown as Resolver<TempoFormValues>, defaultValues: initial as Partial<TempoFormValues> })

  const createMut = useMutation({
    mutationFn: (body: DimTempoCreate) => createTempo(body),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tempo'] }),
  })
  const updateMut = useMutation({
    mutationFn: (vars: { id: number; body: DimTempoUpdate }) => updateTempo(vars.id, vars.body),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tempo'] }),
  })

  const onSubmit = async (data: TempoFormValues) => {
    if (initial?.id) {
      await updateMut.mutateAsync({ id: initial.id, body: data })
    } else {
      await createMut.mutateAsync(data)
    }
    onSuccess()
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">Data</span>
          <input className="w-full rounded-md border bg-background px-2 py-1" placeholder="2025-01-01" {...register('data')} />
          {errors.data && <span className="text-xs text-destructive">{errors.data.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Ano</span>
          <input type="number" className="w-full rounded-md border bg-background px-2 py-1" {...register('ano')} />
          {errors.ano && <span className="text-xs text-destructive">{errors.ano.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Mês</span>
          <input type="number" className="w-full rounded-md border bg-background px-2 py-1" {...register('mes')} />
          {errors.mes && <span className="text-xs text-destructive">{errors.mes.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Trimestre</span>
          <input type="number" className="w-full rounded-md border bg-background px-2 py-1" {...register('trimestre')} />
          {errors.trimestre && <span className="text-xs text-destructive">{errors.trimestre.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Quadrimestre</span>
          <input type="number" className="w-full rounded-md border bg-background px-2 py-1" {...register('quadrimestre')} />
          {errors.quadrimestre && <span className="text-xs text-destructive">{errors.quadrimestre.message}</span>}
        </label>
        <label className="text-sm col-span-2">
          <span className="block text-muted-foreground">Mês (nome)</span>
          <input className="w-full rounded-md border bg-background px-2 py-1" placeholder="Janeiro" {...register('mes_nome')} />
          {errors.mes_nome && <span className="text-xs text-destructive">{errors.mes_nome.message}</span>}
        </label>
      </div>
      <div className="flex justify-end gap-2">
        <button type="submit" disabled={isSubmitting || createMut.isPending || updateMut.isPending} className="rounded-md border bg-primary px-3 py-1 text-sm text-primary-foreground">
          Salvar
        </button>
      </div>
    </form>
  )
}

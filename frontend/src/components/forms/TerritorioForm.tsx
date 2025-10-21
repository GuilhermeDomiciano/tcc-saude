import { useForm, type Resolver } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { createTerritorio, updateTerritorio } from '../../lib/api'
import type { DimTerritorioCreate, DimTerritorioUpdate } from '../../lib/types'

const schema = z.object({
  cod_ibge_municipio: z.string().min(6).max(7).regex(/^\d{6,7}$/g, '6-7 dígitos'),
  nome: z.string().min(1),
  uf: z.string().length(2),
  area_km2: z.coerce.number().optional(),
  pop_censo_2022: z.coerce.number().int().optional(),
  pop_estim_2024: z.coerce.number().int().optional(),
})

export type TerritorioFormValues = z.infer<typeof schema>

type TerritorioFormProps = {
  initial?: Partial<TerritorioFormValues> & { id?: number }
  onSuccess: () => void
}

export default function TerritorioForm({ initial, onSuccess }: TerritorioFormProps) {
  const queryClient = useQueryClient()
  const { register, handleSubmit, formState: { errors, isSubmitting }, setValue } = useForm<TerritorioFormValues>({
    resolver: zodResolver(schema) as unknown as Resolver<TerritorioFormValues>,
    defaultValues: initial as Partial<TerritorioFormValues>,
  })

  const createMut = useMutation({
    mutationFn: (body: DimTerritorioCreate) => createTerritorio(body),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['territorios'] }),
  })
  const updateMut = useMutation({
    mutationFn: (vars: { id: number; body: DimTerritorioUpdate }) => updateTerritorio(vars.id, vars.body),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['territorios'] }),
  })

  const onSubmit = async (data: TerritorioFormValues) => {
    const body = { ...data, uf: data.uf.toUpperCase() }
    if (initial?.id) {
      await updateMut.mutateAsync({ id: initial.id, body })
    } else {
      await createMut.mutateAsync(body)
    }
    onSuccess()
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">IBGE Município</span>
          <input className="w-full rounded-md border bg-background px-2 py-1" placeholder="4300000" {...register('cod_ibge_municipio')} />
          {errors.cod_ibge_municipio && <span className="text-xs text-destructive">{errors.cod_ibge_municipio.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">UF</span>
          <input className="w-full uppercase rounded-md border bg-background px-2 py-1" maxLength={2} {...register('uf')} onChange={(e) => setValue('uf', e.target.value.toUpperCase())} />
          {errors.uf && <span className="text-xs text-destructive">{errors.uf.message}</span>}
        </label>
        <label className="text-sm col-span-2">
          <span className="block text-muted-foreground">Nome</span>
          <input className="w-full rounded-md border bg-background px-2 py-1" placeholder="Município A" {...register('nome')} />
          {errors.nome && <span className="text-xs text-destructive">{errors.nome.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Área (km²)</span>
          <input type="number" step="0.01" className="w-full rounded-md border bg-background px-2 py-1" {...register('area_km2')} />
          {errors.area_km2 && <span className="text-xs text-destructive">{errors.area_km2.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Pop. Censo 2022</span>
          <input type="number" className="w-full rounded-md border bg-background px-2 py-1" {...register('pop_censo_2022')} />
          {errors.pop_censo_2022 && <span className="text-xs text-destructive">{errors.pop_censo_2022.message}</span>}
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Pop. Estim. 2024</span>
          <input type="number" className="w-full rounded-md border bg-background px-2 py-1" {...register('pop_estim_2024')} />
          {errors.pop_estim_2024 && <span className="text-xs text-destructive">{errors.pop_estim_2024.message}</span>}
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

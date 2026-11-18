import { create } from 'zustand'

interface AppState {
  selectedRegionId: number
  setSelectedRegionId: (id: number) => void
  activeLayer: 'risk' | 'rainfall' | 'tide' | 'elevation'
  setActiveLayer: (layer: 'risk' | 'rainfall' | 'tide' | 'elevation') => void
  timeRangeDays: number
  setTimeRangeDays: (days: number) => void
  isDemoMode: boolean
  setDemoMode: (val: boolean) => void
}

export const useAppStore = create<AppState>((set) => ({
  selectedRegionId: 1,
  setSelectedRegionId: (id) => set({ selectedRegionId: id }),
  activeLayer: 'risk',
  setActiveLayer: (layer) => set({ activeLayer: layer }),
  timeRangeDays: 30,
  setTimeRangeDays: (days) => set({ timeRangeDays: days }),
  isDemoMode: true,
  setDemoMode: (val) => set({ isDemoMode: val }),
}))


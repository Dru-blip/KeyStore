import { create } from 'zustand'
import { Vault } from './types'

interface VaultStore {
    vaults: Array<Vault>,
    addVault: (vault: Vault) => void,
    findVault: (id: string) => Vault | undefined,
    addRecord:(vault:Vault, record:any)=>void,
    deleteRecord:(vault:Vault, recordId:string)=>void,
}

export const useVaults = create<VaultStore>((set,get) => ({
    vaults: [],
    addVault: (vault: Vault) => set((state) => ({ vaults: [...state.vaults, vault] })),
    findVault: (id: string) => {
        return get().vaults.find(vault => vault.id === id);
    },
    addRecord: (vault: Vault, record: any) => set((state)=>{
        const vaultIndex=state.vaults.findIndex((v)=>v.id===vault.id);
        state.vaults[vaultIndex].records.push(record);
        const updatedVaults=[...state.vaults];
        return {vaults:updatedVaults}
    }),
    deleteRecord:(vault:Vault,recordId:string)=>set((state)=>{
        const vaultIndex=state.vaults.findIndex((v)=>v.id===vault.id);
        state.vaults[vaultIndex].records=state.vaults[vaultIndex].records.filter((r)=>r.id!==recordId);
        const updatedVaults=[...state.vaults];
        console.log("Updated vaults:", updatedVaults);
        return {vaults:updatedVaults}
    })
}))

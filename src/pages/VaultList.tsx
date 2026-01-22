import { useState } from 'react';
import {
    Container,
    Title,
    Card,
    Text,
    Button,
    Group,
    Stack,
    Modal,
    TextInput,
    PasswordInput,
} from '@mantine/core';
import { IconPlus, IconFolderOpen } from '@tabler/icons-react';
import { useVaults } from '../store';
import { createVault, Vault } from '../types';
import { useNavigate } from "react-router";



export default function VaultList() {
    const vaults=useVaults((state)=>(state.vaults));
    const addVault=useVaults((state)=>(state.addVault));

    const [opened, setOpened] = useState(false);
    const [vaultName, setVaultName] = useState('');
    const [masterPassword, setMasterPassword] = useState('');
    const navigate = useNavigate();

    const handleCreateVault = () => {
        if (vaultName && masterPassword) {
            const newVault: Vault = createVault(vaultName);
            addVault(newVault);
            resetInputState();
            navigate(`/vault/${newVault.id}`);
        }
        //TODO: handle validation errors
    };

    const resetInputState = () => {
        setVaultName('');
        setMasterPassword('');
        setOpened(false);
    }

    const handleOpenVault = (vaultId: string) => {
        //pass
    };

    return (
        <Container size="lg" py="xl">
            <Stack gap="lg">
                <Group justify="space-between" align="center">
                    <Title order={1}>My Vaults</Title>
                    <Button
                        leftSection={<IconPlus size={18} />}
                        onClick={() => setOpened(true)}
                    >
                        Create New Vault
                    </Button>
                </Group>

                <Stack gap="md">
                    {vaults.map((vault) => (
                        <Card key={vault.id} shadow="sm" padding="lg" radius="md" withBorder>
                            <Group justify="space-between" align="center">
                                <Text size="lg" fw={500}>
                                    {vault.name}
                                </Text>
                                <Button
                                    variant="light"
                                    leftSection={<IconFolderOpen size={18} />}
                                    onClick={() => handleOpenVault(vault.id)}
                                >
                                    Open
                                </Button>
                            </Group>
                        </Card>
                    ))}
                </Stack>
            </Stack>

            <Modal
                opened={opened}
                onClose={() => setOpened(false)}
                title="Create New Vault"
                centered
            >
                <Stack gap="md">
                    <TextInput
                        label="Vault Name"
                        placeholder="Enter vault name"
                        value={vaultName}
                        onChange={(e) => setVaultName(e.currentTarget.value)}
                        required
                    />
                    <PasswordInput
                        label="Master Password"
                        placeholder="Enter master password"
                        value={masterPassword}
                        onChange={(e) => setMasterPassword(e.currentTarget.value)}
                        required
                    />
                    <Group justify="flex-end" mt="md">
                        <Button variant="default" onClick={() => setOpened(false)}>
                            Cancel
                        </Button>
                        <Button onClick={handleCreateVault}>Create Vault</Button>
                    </Group>
                </Stack>
            </Modal>
        </Container>
    );
}

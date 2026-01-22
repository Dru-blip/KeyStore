import { useState } from "react";
import { useParams } from "react-router";
import { useVaults } from "../store";
import {
    Container,
    Title,
    Button,
    Group,
    Stack,
    Modal,
    TextInput,
    PasswordInput,
    Card,
    Text,
    ActionIcon,
} from "@mantine/core";
import { IconPlus, IconTrash, IconEdit } from "@tabler/icons-react";
import { createRecord } from "../types";

export default function VaultPage() {
    let { vaultId } = useParams();
    const vaults = useVaults((state) => state.vaults);
    const addRecord = useVaults((state) => state.addRecord);
    const deleteRecord = useVaults((state) => state.deleteRecord);
    const vault = vaults.find(v => v.id === vaultId)!;

    const [opened, setOpened] = useState(false);
    const [recordName, setRecordName] = useState("");
    const [usernameOrEmail, setUsernameOrEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleAddRecord = () => {
        //TODO: validate inputs
        if (recordName && usernameOrEmail && password) {
            const newRecord = createRecord(recordName, usernameOrEmail, password)
            addRecord(vault!, newRecord);
        }
        resetInputState()
    };

    const handleDeleteRecord = (recordId: string) => {
        console.log("Delete record:", recordId);
        deleteRecord(vault!, recordId);
    };

    const handleUpdateRecord = (recordId: string) => {
        // TODO: Implement update logic
        console.log("Update record:", recordId);
    };

    const resetInputState = () => {
        setRecordName("");
        setUsernameOrEmail("");
        setPassword("");
        setOpened(false);
    }

    return (
        <Container size="lg" py="xl">
            <Stack gap="lg">
                <Group justify="space-between" align="center">
                    <Title order={1}>{vault?.name}</Title>
                    <Button
                        leftSection={<IconPlus size={18} />}
                        onClick={() => setOpened(true)}
                    >
                        Add Record
                    </Button>
                </Group>

                <Stack gap="md">
                    {vault?.records.map((record) => (
                        <Card key={record.id} shadow="sm" padding="lg" radius="md" withBorder>
                            <Stack gap="sm">
                                <Group justify="space-between" align="flex-start">
                                    <Stack gap="xs" style={{ flex: 1 }}>
                                        <Text size="lg" fw={600}>
                                            {record.name}
                                        </Text>
                                        <Text size="sm" c="dimmed">
                                            <strong>Username/Email:</strong> {record.usernameOrEmail}
                                        </Text>
                                        <Text size="sm" c="dimmed">
                                            <strong>Password:</strong> {record.password}
                                        </Text>
                                    </Stack>
                                    <Group gap="xs">
                                        <ActionIcon
                                            variant="light"
                                            color="blue"
                                            size="lg"
                                            onClick={() => handleUpdateRecord(record.id)}
                                        >
                                            <IconEdit size={18} />
                                        </ActionIcon>
                                        <ActionIcon
                                            variant="light"
                                            color="red"
                                            size="lg"
                                            onClick={() => handleDeleteRecord(record.id)}
                                        >
                                            <IconTrash size={18} />
                                        </ActionIcon>
                                    </Group>
                                </Group>
                            </Stack>
                        </Card>
                    ))}
                </Stack>
            </Stack>

            <Modal
                opened={opened}
                onClose={() => setOpened(false)}
                title="Add New Record"
                centered
            >
                <Stack gap="md">
                    <TextInput
                        label="Name"
                        placeholder="Enter record name"
                        value={recordName}
                        onChange={(e) => setRecordName(e.currentTarget.value)}
                        required
                    />
                    <TextInput
                        label="Username/Email"
                        placeholder="Enter username or email"
                        value={usernameOrEmail}
                        onChange={(e) => setUsernameOrEmail(e.currentTarget.value)}
                        required
                    />
                    <PasswordInput
                        label="Password"
                        placeholder="Enter password"
                        value={password}
                        onChange={(e) => setPassword(e.currentTarget.value)}
                        required
                    />
                    <Group justify="flex-end" mt="md">
                        <Button variant="default" onClick={() => setOpened(false)}>
                            Cancel
                        </Button>
                        <Button onClick={handleAddRecord}>Add Record</Button>
                    </Group>
                </Stack>
            </Modal>
        </Container>
    );
}

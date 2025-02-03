from abc import ABC, abstractmethod

#classe abstrata
class InventoryItem(ABC):
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    @abstractmethod
    def display_info(self):
        pass

#classe derivada para itens consumíveis
class ConsumableItem(InventoryItem):
    def display_info(self):
        return f"Consumable: {self.name}, Quantity: {self.quantity}"

#classe derivada para itens duráveis
class DurableItem(InventoryItem):
    def display_info(self):
        return f"Durable: {self.name}, Quantity: {self.quantity}"

# Função para carregar inventário do arquivo
def load_inventory(filename):
    inventory = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Divide cada linha em nome, quantidade e tipo de item
                name, quantity, item_type = line.strip().split(',')
                # Adiciona o item apropriado ao inventário com base no tipo
                if item_type == 'Consumable':
                    inventory.append(ConsumableItem(name, int(quantity)))
                elif item_type == 'Durable':
                    inventory.append(DurableItem(name, int(quantity)))
    except FileNotFoundError:
        print("Para já, nao há items.")
    except Exception as e:
        print(f"Erro ao carregar inventário: {e}")
    return inventory

#salvar item no arquivo
def save_inventory(inventory, filename):
    try:
        with open(filename, 'w') as file:
            for item in inventory:
                # Determina o tipo de item para salvar corretamente
                item_type = 'Consumable' if isinstance(item, ConsumableItem) else 'Durable'
                # Escreve o item no arquivo
                file.write(f"{item.name},{item.quantity},{item_type}\n")
        print("Inventário salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar inventário: {e}")

#remover item
def remove_item(inventory):
    name = input("Nome do item a remover: ").strip()
    try:
        quantity_to_remove = int(input("Quantidade a remover: ").strip())
    except ValueError:
        print("Quantidade inválida. Tem de ser um número.")
        return

    #encontrar o item a ser removido
    for item in inventory:
        if item.name == name:
            # Verifica se a quantidade a remover é válida
            if item.quantity >= quantity_to_remove:
                item.quantity -= quantity_to_remove
                # Remove o item do inventário se a quantidade for zero
                if item.quantity == 0:
                    inventory.remove(item)
                print(f"Removido {quantity_to_remove} de {name}.")
            else:
                print(f"Quantidade insuficiente. Apenas {item.quantity} disponível.")
            break
    else:
        print(f"Item '{name}' não encontrado no inventário.")

#calcular a quantidade total de itens
def calculate_and_display_totals(inventory):
    total_consumable = 0
    total_durable = 0
    item_totals = {}

    # Calcula a quantidade total de itens por tipo e por nome
    for item in inventory:
        if isinstance(item, ConsumableItem):
            total_consumable += item.quantity
        elif isinstance(item, DurableItem):
            total_durable += item.quantity

        # Atualiza o total de itens por nome
        if item.name in item_totals:
            item_totals[item.name] += item.quantity
        else:
            item_totals[item.name] = item.quantity

    # Exibe a quantidade total por item
    print("\nQuantidade total por item:")
    for name, quantity in item_totals.items():
        print(f"{name}: {quantity}")

    # Exibe a quantidade total por tipo
    print("\nQuantidade total por tipo:")
    print(f"Consumível: {total_consumable}")
    print(f"Durável: {total_durable}")

    # Exibe a quantidade total de itens no inventário
    total_quantity = total_consumable + total_durable
    print(f"\nQuantidade total em inventório: {total_quantity}")

#adicionar item
def add_item(inventory):
    item_type=input("Consumivel (c) ou duravel (d)? ").strip().lower()
    name=input("Nome do item: ").strip()
    try:
        quantity = int(input("Quantidade: ").strip())
    except ValueError:
        print("Quantidade inválida. Tem de ser um número.")
        return

    # Adiciona o item apropriado ao inventário com base no tipo
    if item_type=='c':
        inventory.append(ConsumableItem(name, quantity))
    elif item_type=='d':
        inventory.append(DurableItem(name, quantity))
    else:
        print("Tipo inválido. 'c' para consumivel ou 'd' para duravel.")

#mudar o tipo de item
def change_item_type(inventory):
    name = input("Nome do item a mudar de tipo: ").strip()
    
    # Percorre o inventário para encontrar o item a ser alterado
    for item in inventory:
        if item.name == name:
            new_quantity = item.quantity
            # Verifica o tipo atual do item e o converte para o outro tipo
            if isinstance(item, DurableItem):
                inventory.remove(item)
                inventory.append(ConsumableItem(name, new_quantity))
                print(f"Item '{name}' mudou de tipo para 'Consumível'.")
            elif isinstance(item, ConsumableItem):
                inventory.remove(item)
                inventory.append(DurableItem(name, new_quantity))
                print(f"Item '{name}' mudou de tipo para 'Durável'.")
            break
    else:
        print(f"Item '{name}' não encontrado no inventário.")

#programa principal
def main():
    inventory = load_inventory('inventory.txt')

    while True:
        #menu
        action = input("\nQuer adicionar items (add)\nRemover items (remove)\nSaber o total do inventario (total)\nMudar tipo de item (change)\nOu gravar e sair (exit)? ").strip().lower()
        if action == 'add':
            add_item(inventory)
        elif action == 'remove':
            remove_item(inventory)
        elif action == 'total':
            calculate_and_display_totals(inventory)
        elif action == 'change':
            change_item_type(inventory)
        elif action == 'exit':
            save_inventory(inventory, 'inventory.txt')
            print("\nInventorio guardado. Xau.")
            break
        else:
            print("\nOpcao invalida. Tente novamente com 'add', 'remove', 'total', 'change' ou 'exit'.")

if __name__ == "__main__":
    main()
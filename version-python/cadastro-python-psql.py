import tkinter as tk
from tkinter import ttk
import psycopg2 

class ClienteApp(tk.Tk):
    def __init__(self):
        super().__init__()
 
        self.title("Gerenciamento de Clientes")
        self.geometry("800x600")

        self.initialize_db()
        self.create_widgets()
        self.listar_clientes()

    def initialize_db(self):
        self.conn = psycopg2.connect(
            dbname="clientedb",
            user="postgres",
            password="giovanna",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                endereco VARCHAR(255),
                rede_social VARCHAR(100),
                email VARCHAR(100) NOT NULL,
                data_cadastro DATE NOT NULL
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Frame para o formulário de edição
        self.edit_frame = ttk.Frame(self)
        self.edit_frame.pack(pady=20)

        # Labels e Entradas para os campos do cliente
        ttk.Label(self.edit_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        self.nome_entry = ttk.Entry(self.edit_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.edit_frame, text="Endereço:").grid(row=1, column=0, sticky=tk.W)
        self.endereco_entry = ttk.Entry(self.edit_frame, width=40)
        self.endereco_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.edit_frame, text="Rede Social:").grid(row=2, column=0, sticky=tk.W)
        self.rede_social_entry = ttk.Entry(self.edit_frame, width=40)
        self.rede_social_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.edit_frame, text="Email:").grid(row=3, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(self.edit_frame, width=40)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.edit_frame, text="Data de Cadastro:").grid(row=4, column=0, sticky=tk.W)
        self.data_cadastro_entry = ttk.Entry(self.edit_frame, width=40)
        self.data_cadastro_entry.grid(row=4, column=1, padx=5, pady=5)

        # Botões para salvar e cancelar
        ttk.Button(self.edit_frame, text="Salvar", command=self.salvar_cliente).grid(row=5, column=0, padx=5, pady=10)
        ttk.Button(self.edit_frame, text="Cancelar", command=self.limpar_formulario).grid(row=5, column=1, padx=5, pady=10)

        # Frame para listar os clientes
        self.list_frame = ttk.Frame(self)
        self.list_frame.pack(padx=20, pady=10)

        # Treeview para listar os clientes
        self.clientes_tree = ttk.Treeview(self.list_frame, columns=('ID', 'Nome', 'Endereço', 'Rede Social', 'Email', 'Data de Cadastro'), show='headings')
        self.clientes_tree.heading('ID', text='ID')
        self.clientes_tree.heading('Nome', text='Nome')
        self.clientes_tree.heading('Endereço', text='Endereço')
        self.clientes_tree.heading('Rede Social', text='Rede Social')
        self.clientes_tree.heading('Email', text='Email')
        self.clientes_tree.heading('Data de Cadastro', text='Data de Cadastro')
        self.clientes_tree.pack()

        # Configuração de evento para selecionar um cliente na Treeview
        self.clientes_tree.bind('<ButtonRelease-1>', self.carregar_cliente_selecionado)

    def listar_clientes(self):
        self.clientes_tree.delete(*self.clientes_tree.get_children())
        self.cursor.execute('SELECT id, nome, endereco, rede_social, email, data_cadastro FROM clientes')
        for cliente in self.cursor.fetchall():
            self.clientes_tree.insert('', 'end', values=cliente)

    def carregar_cliente_selecionado(self, event):
        item = self.clientes_tree.selection()[0]
        cliente_id = self.clientes_tree.item(item, 'values')[0]
        self.cursor.execute('SELECT nome, endereco, rede_social, email, data_cadastro FROM clientes WHERE id=%s', (cliente_id,))
        cliente = self.cursor.fetchone()
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, cliente[0])
        self.endereco_entry.delete(0, tk.END)
        self.endereco_entry.insert(0, cliente[1])
        self.rede_social_entry.delete(0, tk.END)
        self.rede_social_entry.insert(0, cliente[2])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, cliente[3])
        self.data_cadastro_entry.delete(0, tk.END)
        self.data_cadastro_entry.insert(0, cliente[4])

    def salvar_cliente(self):
        nome = self.nome_entry.get()
        endereco = self.endereco_entry.get()
        rede_social = self.rede_social_entry.get()
        email = self.email_entry.get()
        data_cadastro = self.data_cadastro_entry.get()

        if nome and email and data_cadastro:
            cliente = (nome, endereco, rede_social, email, data_cadastro)
            if self.clientes_tree.selection():
                cliente_id = self.clientes_tree.item(self.clientes_tree.selection()[0], 'values')[0]
                self.cursor.execute('''
                    UPDATE clientes SET nome=%s, endereco=%s, rede_social=%s, email=%s, data_cadastro=%s
                    WHERE id=%s
                ''', (*cliente, cliente_id))
            else:
                self.cursor.execute('''
                    INSERT INTO clientes (nome, endereco, rede_social, email, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s)
                ''', cliente)
            self.conn.commit()
            self.listar_clientes()
            self.limpar_formulario()
        else:
            print("Preencha todos os campos obrigatórios!")

    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
        self.endereco_entry.delete(0, tk.END)
        self.rede_social_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.data_cadastro_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = ClienteApp()
    app.mainloop()

class UserDbStore {
    constructor(dbName) {
        this.dbName = dbName;

        if (!localStorage.getItem(this.dbName)) {
            this._initializeDb();
        }
    }

    _initializeDb() {
        const initialData = {
            users: [
                { id_Registro: 1, Usuario: "Carlos", Contraseña: this._hashPassword("Carlos"), Entrada: "", Salida: "", Rol: "User", Identidad: "false" },
                { id_Registro: 2, Usuario: "Juan", Contraseña: this._hashPassword("Juan"), Entrada: "", Salida: "", Rol: "Admin", Identidad: "false" },
                { id_Registro: 3, Usuario: "Wil", Contraseña: this._hashPassword("Wil"), Entrada: "", Salida: "", Rol: "Admin", Identidad: "false" }
            ]
        };
        localStorage.setItem(this.dbName, JSON.stringify(initialData));
    }

    _getDb() {
        const db = JSON.parse(localStorage.getItem(this.dbName));
        if (!db || !db.users) {
            this._initializeDb();
            return JSON.parse(localStorage.getItem(this.dbName));
        }
        return db;
    }

    _saveDb(data) {
        localStorage.setItem(this.dbName, JSON.stringify(data));
    }

    _hashPassword(password) {
        // Esta función será usada por Identity, no por UserDbStore
        return btoa(password);
    }

    addUser(user) {
        const db = this._getDb();

        if (!user.id_Registro) {
            user.id_Registro = db.users.length + 1; // Asigna un ID único.
        }

        if (db.users.find(u => u.Usuario === user.Usuario)) {
            console.error("Ya existe un usuario con ese nombre de usuario.");
            return;
        }

        db.users.push(user);
        this._saveDb(db);
        console.log("Usuario agregado:", user);
    }

    updateUser(id, updatedUser) {
        const db = this._getDb();

        const index = db.users.findIndex(u => u.id_Registro === id);
        if (index !== -1) {
            updatedUser.id_Registro = id;
            db.users[index] = updatedUser;
            this._saveDb(db);
            console.log("Usuario actualizado:", updatedUser);
        } else {
            console.error("No se encontró un usuario con el ID:", id);
        }
    }

    deleteUser(id) {
        const db = this._getDb();
        db.users = db.users.filter(u => u.id_Registro !== id);
        this._saveDb(db);
        console.log("Usuario eliminado con ID:", id);
    }

    getUsers() {
        return this._getDb().users;
    }

    getUserById(id) {
        return this._getDb().users.find(u => u.id_Registro === id);
    }

    getUserByUsername(username) {
        return this._getDb().users.find(u => u.Usuario === username);
    }

    clearDbStore() {
        localStorage.removeItem(this.dbName);
        this._initializeDb();
        console.log("Base de datos de usuarios limpiada.");
    }

    static getInstance(dbName) {
        if (!UserDbStore.instance) {
            UserDbStore.instance = new UserDbStore(dbName);
        }
        return UserDbStore.instance;
    }
}

 
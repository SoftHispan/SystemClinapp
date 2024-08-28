class DbLocalStore {
    constructor(dbName) {
        this.dbName = dbName;

        if (!localStorage.getItem(this.dbName)) {
            this._initializeDb();
        }
    }

    _initializeDb() {
        const initialData = { records: [] };
        localStorage.setItem(this.dbName, JSON.stringify(initialData));
    }

    _getDb() {
        const db = JSON.parse(localStorage.getItem(this.dbName));
        if (!db || !db.records) {
            this._initializeDb();
            return JSON.parse(localStorage.getItem(this.dbName));
        }
        return db;
    }

    _saveDb(data) {
        localStorage.setItem(this.dbName, JSON.stringify(data));
    }

    showDatabaseState(message) {
        const records = this.getRecords();
        console.log(message, records);
    }

    _validateAndConvertToJSON(input) {
        if (typeof input === "object" && input !== null) {
            try {
                return JSON.stringify(input);
            } catch (e) {
                console.error("Error al convertir objeto a JSON:", e);
                return null;
            }
        }

        if (typeof input === "string") {
            try {
                return JSON.stringify(JSON.parse(input));
            } catch (e) {
                console.error("Cadena no es un JSON válido:", e);
                return null;
            }
        }

        console.error("Tipo de dato no soportado. Se esperaba un objeto o cadena JSON.");
        return null;
    }

    getNumberOfProperties(json) {
        let parsedObject;

        if (typeof json === "string") {
            try {
                parsedObject = JSON.parse(json);
            } catch (e) {
                console.error("Error al analizar JSON:", e);
                return 0;
            }
        } else if (typeof json === "object" && json !== null) {
            parsedObject = json;
        } else {
            console.error("Tipo de dato no soportado para contar propiedades.");
            return 0;
        }

        return Object.keys(parsedObject).length;
    }

    addRecord(record) {
        const validRecordJson = this._validateAndConvertToJSON(record);
        if (!validRecordJson) {
            console.error("Error al validar o convertir el registro a JSON.");
            return;
        }

        this.showDatabaseState("Antes de crear el registro:");
        const db = this._getDb();

        const parsedRecord = JSON.parse(validRecordJson);
        if (!parsedRecord.id_Registro) {
            console.error("El registro debe contener un campo 'id_Registro'.");
            return;
        }

        if (!Array.isArray(db.records)) {
            db.records = [];
        }

        const existingRecord = db.records.find(rec => rec.id_Registro === parsedRecord.id_Registro);
        if (existingRecord) {
            console.error("Ya existe un registro con el mismo ID.");
            return;
        }

        db.records.push(parsedRecord);
        this._saveDb(db);
        this.showDatabaseState("Después de crear el registro:");
    }

    updateRecord(id, updatedRecord) {
        const validRecordJson = this._validateAndConvertToJSON(updatedRecord);
        if (!validRecordJson) {
            console.error("Error al validar o convertir el registro a JSON.");
            return;
        }

        this.showDatabaseState("Antes de actualizar el registro:");
        const db = this._getDb();

        const parsedRecord = JSON.parse(validRecordJson);
        const index = db.records.findIndex(rec => rec.id_Registro === id);
        if (index !== -1) {
            parsedRecord.id_Registro = id;
            db.records[index] = parsedRecord;
            this._saveDb(db);
            this.showDatabaseState("Después de actualizar el registro:");
        } else {
            console.error("No se encontró un registro con el ID:", id);
        }
    }

    deleteRecord(id) {
        this.showDatabaseState("Antes de eliminar el registro:");
        const db = this._getDb();
        db.records = db.records.filter(rec => rec.id_Registro !== id);
        this._saveDb(db);
        this.showDatabaseState("Después de eliminar el registro:");
    }

    getRecords() {
        return this._getDb().records;
    }

    getRecordById(id) {
        return this._getDb().records.find(rec => rec.id_Registro === id);
    }

    // Método para limpiar toda la base de datos
    clearDbStore() {
        this._initializeDb();
        console.log("Base de datos limpiada.");
        this.showDatabaseState("Estado de la base de datos después de ser limpiada:");
    }

    static getInstance(dbName) {
        if (!DbLocalStore.instance) {
            DbLocalStore.instance = new DbLocalStore(dbName);
        }
        return DbLocalStore.instance;
    }
}
 

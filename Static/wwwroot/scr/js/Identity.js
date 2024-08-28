class Identity {
  static roles = ["Admin", "User", "Guest"]; // Roles globales

  constructor(userDbStore) {
    this.userDbStore = userDbStore;
  }

  async authenticate(username, password) {
    if (!this.userDbStore) {
      console.error("UserDbStore no está inicializado correctamente.");
      return false;
    }

    // Validación básica de entradas
    if (!username || !password) {
      console.error("Usuario o contraseña no pueden estar vacíos.");
      return false;
    }

    const user = this.userDbStore.getUserByUsername(username);

    if (!user) {
      console.error("Usuario no encontrado.");
      return false;
    }

    const hashedPassword = await this._hashPassword(password);

    if (hashedPassword === user.Contraseña) {
      console.log("Autenticación exitosa para el usuario:", username);

      if (user.Identidad === "false") {
        const now = new Date();
        user.Identidad = "true";
        user.Entrada = now;
        user.Salida = new Date(now.getTime() + 1 * 60 * 1000); // Añadir 1 minuto

        this.userDbStore.updateUser(user.id_Registro, user);
      }

      return true;
    }

    console.error("Fallo en la autenticación para el usuario:", username);
    return false;
  }

  checkSession() {
    const users = this.userDbStore.getUsers(); // Cambiado a getUsers()
    const now = new Date();

    for (let user of users) {
      if (user.Identidad === "true") {
        if (now >= new Date(user.Entrada) && now <= new Date(user.Salida)) {
          console.log("La sesión del usuario", user.Usuario, "es válida.");
          return true;
        } else {
          console.error("La sesión del usuario", user.Usuario, "ha caducado.");

          // Restablecer propiedades al caducar la sesión
          this.clearUser(user);
          return false;
        }
      }
    }
    console.log("No hay usuarios con sesión activa.");
    return false;
  }

  checkRol(role) {
    return Identity.roles.includes(role);
  }

  async register(user) {
    if (!this._validateUserRecord(user)) {
      console.error("El registro de usuario no es válido.");
      return;
    }

    user.Contraseña = await this._hashPassword(user.Contraseña);
    this.userDbStore.addUser(user);
  }

  clearUser(user) {
    user.Identidad = "false";
    user.Entrada = "";
    user.Salida = "";
    this.userDbStore.updateUser(user.id_Registro, user);
    sessionStorage.removeItem("UserNameAuthenticated");
    console.log("Usuario desautenticado y sesión eliminada.");
  }

  _validateUserRecord(user) {
    const requiredFields = [
      "Usuario",
      "Contraseña",
      "Entrada",
      "Salida",
      "Rol",
      "Identidad",
    ];
    for (let field of requiredFields) {
      if (!user.hasOwnProperty(field)) {
        console.error(`El campo ${field} es obligatorio.`);
        return false;
      }
    }

    if (user.Contraseña.length < 6) {
      console.error("La contraseña debe tener al menos 6 caracteres.");
      return false;
    }

    if (isNaN(Date.parse(user.Entrada)) || isNaN(Date.parse(user.Salida))) {
      console.error("Las fechas de Entrada y Salida deben ser válidas.");
      return false;
    }

    if (!Identity.roles.includes(user.Rol)) {
      // Validar el rol usando la lista global
      console.error("El rol especificado no es válido.");
      return false;
    }

    return true;
  }

  async _hashPassword(password) {
    // Simulación de una función de hash para propósitos de ejemplo
    return btoa(password); // Reemplaza con un hash real en producción
  }

  static getInstance(userDbStore) {
      if (!Identity.instance) {
        Identity.instance = new Identity(userDbStore);
      }
      return Identity.instance;
  }
  
}

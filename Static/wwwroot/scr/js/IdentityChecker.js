class IdentityChecker {
  constructor(identity) {
    if (IdentityChecker.instance) {
      return IdentityChecker.instance;
    }

    this.identity = identity;
    this.timer = null;
    this.interval = 120000; // Intervalo de 1 minuto (60000 milisegundos)
    this.isRunning = false;
    this.startTime = null;

    IdentityChecker.instance = this;
  }

  async authenticateUser(username, password) {
    if (this.isRunning) {
      console.error(
        "Ya hay un usuario autenticado. No se puede autenticar otro usuario."
      );
      return false;
    }

    const isAuthenticated = await this.identity.authenticate(
      username,
      password
    );
    if (isAuthenticated) {
      console.log("Usuario autenticado. Iniciando verificación de sesión.");
      this.startTime = new Date(); // Registrar la hora de inicio
      this.startChecking(); // Iniciar la verificación periódica si la autenticación es exitosa
      return true;
    } else {
      console.error(
        "Autenticación fallida. Verificación de sesión no iniciada."
      );
      return false;
    }
  }

  startChecking() {
    if (this.isRunning) {
      console.log("La verificación de sesión ya está en funcionamiento.");
      return;
    }

    this.timer = setInterval(() => this.checkIdentity(), this.interval);
    this.isRunning = true;
    this.startTime = new Date(); // Reiniciar el tiempo de inicio al comenzar el chequeo
    console.log("Temporizador iniciado para verificar la sesión del usuario.");
  }

  async checkIdentity() {
    const currentTime = new Date();
    const elapsedTime = Math.floor((currentTime - this.startTime) / 1000); // Tiempo transcurrido en segundos
    console.log(`Tiempo transcurrido: ${elapsedTime} segundos`);

    const isValidSession = await this.identity.checkSession();

    if (!isValidSession) {
      console.error("Sesión inválida o caducada. Deteniendo la verificación.");
      this.stopChecking();
      // Utiliza las rutas definidas en `appConfig`
      window.location.href = window.appConfig.loginUrl;
      const userDbInstance = UserDbStore.getInstance("userDbStore");
      userDbInstance.clearDbStore();
      alert("La sesion a expirado, sera redireccionado a la pagina Login...");
    } else {
      console.log("Sesión válida. Continuando la verificación.");
    }
  }

  stopChecking() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
      this.isRunning = false;
      console.log("Temporizador detenido.");
    }
  }

  clearUser() {
    this.identity.clearUser();
    this.stopChecking();

    console.log("Usuario desautenticado y temporizador detenido.");
  }
  static getInstance(identity) {
      if (!IdentityChecker.instance) {
        IdentityChecker.instance = new IdentityChecker(identity);
      }
      return IdentityChecker.instance;
  }
}

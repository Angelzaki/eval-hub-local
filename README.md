<div align="center">

# eval-hub-local

**Dashboard local de labs de IA** · Angel Salazar

`escanea results/ → HTML + JSON`

</div>

---

### `$ whoami`

Un solo tablero para ver qué labs ya tienen métricas.  
Sin cloud, sin auth, abre el HTML en el navegador.

---

### `$ ./hub.sh`

Desde este repo:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest
python -m eval_hub --workspace ..
```

Abre `results/dashboard.html`.

---

Hecho en Lima · Angel Salazar · CIP 404730

const API_URL = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", () => {
    loadAppointments();

    const form = document.getElementById("appointmentForm");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        const appointment = {
            nom: formData.get("nom"),
            telefon: formData.get("telefon"),
            correu: formData.get("correu"),
            matricula: formData.get("matricula"),
            model: formData.get("model"),
            any_vehicle: formData.get("any_vehicle"),
            data_cita: formData.get("data_cita"),
            servei: formData.get("servei")
        };

        try {
            const response = await fetch(`${API_URL}/appointments`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(appointment)
            });

            if (response.ok) {
                document.getElementById("message").textContent = "Cita creada correctament";
                form.reset();
                loadAppointments();
            } else {
                document.getElementById("message").textContent = "Error en crear la cita";
            }
        } catch (error) {
            document.getElementById("message").textContent = "No es pot connectar amb l'API";
        }
    });
});


async function loadAppointments() {
    const list = document.getElementById("appointmentsList");

    try {
        const response = await fetch(`${API_URL}/appointments`);
        const appointments = await response.json();

        list.innerHTML = "";

        appointments.forEach(cita => {
            const div = document.createElement("div");
            div.classList.add("appointment");

            div.innerHTML = `
                <strong>${cita.nom}</strong><br>
                Telèfon: ${cita.telefon}<br>
                Vehicle: ${cita.matricula} - ${cita.model} (${cita.any_vehicle})<br>
                Data: ${cita.data_cita}<br>
                Servei: ${cita.servei}<br>
                Estat: ${cita.estat}
            `;

            list.appendChild(div);
        });

    } catch (error) {
        list.innerHTML = "No es poden carregar les cites.";
    }
}
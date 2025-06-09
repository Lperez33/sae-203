<?php
// Connexion à la base SQLite
$db = new PDO('sqlite:mqtt.db');

// Récupération de la date choisie via GET, ou toutes les données si "all"
$date = isset($_GET['date']) ? $_GET['date'] : 'all';

// Préparation de la requête SQL selon le filtre
if ($date === 'all') {
    $stmt = $db->prepare("SELECT api_time, query_time, temperature, windspeed, winddirection FROM weather ORDER BY api_time ASC");
    $stmt->execute();
} else {
    $stmt = $db->prepare("SELECT api_time, query_time, temperature, windspeed, winddirection FROM weather WHERE DATE(api_time) = :date ORDER BY api_time ASC");
    $stmt->execute([':date' => $date]);
}

$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Préparer les données pour Chart.js
$labels = [];
$temperature = [];
$windspeed = [];
$winddirection = [];

foreach ($rows as $row) {
    // On peut formater api_time en heure seulement
    $labels[] = date('H:i', strtotime($row['api_time']));
    $temperature[] = $row['temperature'];
    $windspeed[] = $row['windspeed'];
    $winddirection[] = $row['winddirection'];
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Météo Bordeaux</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<h1>Données météo pour Bordeaux</h1>

<form method="get" action="">
    <label for="date">Choisir une date :</label>
    <input type="date" id="date" name="date" value="<?= ($date !== 'all') ? htmlspecialchars($date) : '' ?>">
    <button type="submit">Filtrer</button>
    <button type="submit" name="date" value="all">Tout afficher</button>
</form>

<canvas id="weatherChart" width="900" height="400"></canvas>

<script>
const ctx = document.getElementById('weatherChart').getContext('2d');
const weatherChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: <?= json_encode($labels) ?>,
        datasets: [
            {
                label: 'Température (°C)',
                data: <?= json_encode($temperature) ?>,
                borderColor: 'rgb(255, 99, 132)',
                fill: false,
                yAxisID: 'y',
            },
            {
                label: 'Vitesse du vent (m/s)',
                data: <?= json_encode($windspeed) ?>,
                borderColor: 'rgb(54, 162, 235)',
                fill: false,
                yAxisID: 'y1',
            },
            {
                label: 'Direction du vent (°)',
                data: <?= json_encode($winddirection) ?>,
                borderColor: 'rgb(255, 206, 86)',
                fill: false,
                yAxisID: 'y2',
            }
        ]
    },
    options: {
    interaction: {
        mode: 'index',
        intersect: false,
    },
    stacked: false,
    scales: {
        y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: { display: true, text: 'Température (°C)' }
        },
        y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: { display: true, text: 'Vitesse du vent (m/s)' },
            grid: { drawOnChartArea: false },
            min: 0,
            suggestedMax: 10
        },
        y2: {
            type: 'linear',
            display: true,
            position: 'right',
            title: { display: true, text: 'Direction du vent (°)' },
            grid: { drawOnChartArea: false },
            min: 0,
            max: 360,
            ticks: { stepSize: 45 }
        }
    }
}

});
</script>

</body>
</html>

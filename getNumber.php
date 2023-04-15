<?php
$db = new SQLite3("db.sqlite");

if (!$db) {
    die("Erreur de connexion à la base de données");
}

$result = $db->query("SELECT nombre_de_personne FROM compeurDB WHERE id = 1");

if ($result) {
    $row = $result->fetchArray(SQLITE3_ASSOC);

    if ($row) {
        header('Content-Type: application/json');
        echo json_encode($row);
    } else {
        echo "Aucun résultat trouvé pour l'ID 1";
    }
} else {
    echo "Erreur lors de la requête SQL";
}

$db->close();
?>

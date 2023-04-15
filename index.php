<?php
function get_nombre_de_personne() {
    $db = new SQLite3('db.sqlite');

    if (!$db) {
        die("Erreur de connexion à la base de données");
    }

    $result = $db->query("SELECT nombre_de_personne FROM compeurDB WHERE id = 1");

    if ($result) {
        $row = $result->fetchArray(SQLITE3_ASSOC); //on récupère le nb de personne dans un tableau associatif

        if ($row) {
            $db->close();

            return $row['nombre_de_personne'];
        }
    }
    $db->close();

    return "Erreur";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Compteur CMI</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            function getNombreDePersonne() {
                $.ajax({
                    url: 'getNumber.php',
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        $('#nombre_de_personne').html(data.nombre_de_personne);
                        $('progress').attr('value', data.nombre_de_personne); // Mettre à jour la valeur de la barre de progression
                    }
                });
            }
            setInterval(getNombreDePersonne, 100); // Correction de la valeur de l'intervalle à 1000 ms pour 1 seconde
        });
    </script>
</head>
<body>
    <h1>Nombre de personnes : </h1>
    <?php
    $max = 50;
    ?>
    <div>
        <h2><span id="nombre_de_personne"><?php echo get_nombre_de_personne(); ?></span>  <?php echo '/ ' . $max ?></h2>
        <progress value="<?php echo get_nombre_de_personne(); ?>" max="<?php echo $max?>"></progress>
    </div>
</body>
</html>

window.addEventListener('DOMContentLoaded', function () {
    let selectedElement = [];
    var FirstClick = true;
    var FirstClickPlayer = true;
    document.querySelectorAll('.alliance').forEach((element) => {
        element.addEventListener('click', () => {
            if (selectedElement.indexOf(element.dataset.allianceId) === -1) {
                selectedElement.push(element.dataset.allianceId)
                element.classList.add('selected')
                element.querySelector('input').checked = true;
            } else {
                var index = selectedElement.indexOf(element.dataset.allianceId);
                if (index > -1) {
                    selectedElement.splice(index, 1)
                }
                element.classList.remove('selected')
                element.querySelector('input').checked = false;
            }
        })
    })

    document.querySelector('#validate').addEventListener('click', () => {
        selectedElement.forEach((alliance_id) => {
            changeColorByAllianceId(alliance_id, document.querySelector('#picker').value);
            document.querySelector('[data-alliance-id="' + alliance_id + '"] .legend').style.backgroundColor = document.querySelector('#picker').value
            document.querySelector('[data-alliance-id="' + alliance_id + '"]').classList.remove('selected')
            document.querySelector('[data-alliance-id="' + alliance_id + '"] input').checked = false
        })

        selectedElement = []
    })

    function changeColorByAllianceId(alliance_id, color) {
        map.eachLayer(function (layer) {
            if (layer instanceof L.Circle && layer.alliance_id == alliance_id) {
                layer.setStyle({ color: color })
                layer.setStyle({'opacity':1, 'fillOpacity':1})
            }
        })
    }

    document.querySelector('#hide-island').addEventListener('click', () => {
       
        if(!FirstClick){
            map.eachLayer(function(layer) {
                if(layer instanceof L.ImageOverlay && layer.type == 'island'){
                    layer.setOpacity(document.querySelector('#hide-island').checked ? 1 : 0)
                } 
            })
            
        } else {
            let xhr = new XMLHttpRequest();

            // Making our connection  
            let url = 'http://127.0.0.1:8000/loadMainIslands';
            xhr.open("GET", url, true);
            // function execute after request is successful 
            xhr.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    JSON.parse(this.responseText).forEach(island => {
                        var imageUrl = '../static/img/' + img_matrix[island.isaland_type]['img'];
                        var image = new Image();
                        image.src = imageUrl;
                        image.onload = function () {
                            var width = image.width;
                            var height = image.height;
            
                            var imageBounds = [
                                [-island.y - height / 380 - img_matrix[island.isaland_type]['xOffset'], island.x + width / 380 + img_matrix[island.isaland_type]['yOffset']],
                                [-island.y + height / 380 - img_matrix[island.isaland_type]['xOffset'], island.x - width / 380 + img_matrix[island.isaland_type]['yOffset']]
                            ];
            
                            var islandLeaflet = L.imageOverlay(imageUrl, imageBounds, { zIndex: 2 });
                            islandLeaflet.type = 'island';
                            islandLeaflet.addTo(map);
                        };
                    });
                }
            }
            xhr.send();
            FirstClick = false;
        }
    })

    document.querySelector('#hide-no-colors').addEventListener('click', () => {
        map.eachLayer(function (layer) {
            if (layer instanceof L.Circle && layer.options.color == '#5c5c5c') {
                opacity = document.querySelector('#hide-no-colors').checked ? 0 : 1
                layer.setStyle({'opacity':opacity, 'fillOpacity':opacity})
            }
        })
    })

    document.querySelector('#load-all').addEventListener('click', () => {
        let xhr = new XMLHttpRequest();

        // Making our connection  
        let url = 'http://127.0.0.1:8000/loadRemainsTowns';
        xhr.open("GET", url, true);

        // function execute after request is successful 
        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                JSON.parse(this.responseText).forEach(town => {
                    var offsets = matrix.filter(item => item.posOnIsland == town.number_on_island && item.islandType == town.isaland_type);
                    var allianceColor
                    if(legend = document.querySelector('[data-alliance-id="' + town.alliance_id + '"] .legend')){
                        allianceColor = legend.style.backgroundColor;   
                    }

                    if(!allianceColor){
                        allianceColor = '#5c5c5c';
                    }

                    circle = L.circle(
                        [-town.island_y + (offsets[0].yOffset * ratio), town.island_x + (offsets[0].xOffset * ratio)],
                        { zIndex: 3, radius: 0.1, color: allianceColor, fillOpacity: 1 }
                    );

                    
                    
                    circle.alliance_id = town.alliance_id;
                    circle.player_id = town.player_id;
                    if (town.alliance_name) {
                        circle.bindTooltip(
                            '<img src="../static/img/player.png" />' + town.player_name + '<br>'
                            + '<img src="../static/img/ally.png" />' + town.alliance_name + '<br>'
                            + '<img src="../static/img/points.png" />' + town.points + 'pts'
                        );
                    } else {
                        circle.bindTooltip(
                            '<img src="../static/img/player.png" />' + town.player_name + '<br>'
                            + '<img src="../static/img/points.png" />' + town.points + 'pts'
                        );
                    }
                    circle.addTo(map)
                });
            }
        }
        // Sending our request 
        xhr.send();

        document.querySelector('#load-all').disabled = true;
    })
});

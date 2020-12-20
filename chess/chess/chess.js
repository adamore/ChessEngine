var size = 0.75 * Math.min($(window).height(), $(window).width());

$('#board').width(size);

var board;
var game = new Chess();
var $status = $('#status');
var $fen = $('#fen');
var $pgn = $('#pgn');
var gameId;

$.getJSON('https://chess-engine-api.herokuapp.com/create-game', function (data) {
    gameId = data.game_id;
}).fail(function (error) {
    window.alert('Apologies, there was an error on the server.');
});

function onDragStart(source, piece, position, orientation) {
    if (game.game_over()) return false

    // do not allow user to move the computer's side
    if (game.turn() === 'b') return false

    // only pick up pieces for the side to move
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false
    }
}

function onDrop(source, target) {
    // see if the move is legal
    var move = game.move({
        from: source,
        to: target,
        promotion: 'q' // always promote to a queen for simplicity
    });

    // illegal move
    if (move === null) return 'snapback';
}

function onSnapEnd(source, target) {
    board.position(game.fen());
    updateStatus(`${source}${target}`);
}

function getComputerMove(moveString) {
    $('#computerloading').css('visibility', 'visible');
    $('#board').css('cursor', 'not-allowed');

    $.getJSON(`https://chess-engine-api.herokuapp.com/make-white-move?game_id=${gameId}&move=${moveString}`, function (data) {
        var fromString = data.move.substring(0, 2);
        var toString = data.move.substring(2, 4);

        var move = game.move({
            from: fromString,
            to: toString,
            promotion: 'q'
        });

        board.position(game.fen());

        updateStatus('', true);

        $('#computerloading').css('visibility', 'hidden');
        $('#board').css('cursor', 'default');
    }).fail(function () {
        window.alert("Apologies, there was an error on the server.");
        location.reload();
    });
}

function updateStatus(moveString, wasComputer = false) {
    var status = '';
    var moveColor = 'White';
    if (game.turn() === 'b') {
        moveColor = 'Computer';
    }
    if (game.in_checkmate()) {
        status = 'Game over, ' + moveColor + ' is in checkmate.';
    } else if (game.in_draw()) {
        status = 'Game over, drawn position';
    } else {
        status = moveColor + ' to move';
        if (game.in_check()) {
            status += ', ' + moveColor + ' is in check';
        }
    }

    $status.html(status);
    $fen.html(game.fen());
    $pgn.html(game.pgn());

    if (!wasComputer && !game.in_checkmate() && !game.in_draw()) {
        getComputerMove(moveString);
    }

    if (game.in_checkmate() || game.in_draw()) {
        window.alert(status);
    }
}

var config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
};

var board = Chessboard('board', config);
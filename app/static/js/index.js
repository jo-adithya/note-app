let sidebar = document.querySelector('.sidebar');
let sideFile = document.querySelector('.file-manager');
let create = document.querySelector('#create');

// following are the code to change sidebar button(optional)
function menuBtnChange() {
  if (sidebar.classList.contains('open')) {
    closeBtn.classList.replace('bx-menu', 'bx-menu-alt-right'); //replacing the iocns class
  } else {
    closeBtn.classList.replace('bx-menu-alt-right', 'bx-menu'); //replacing the iocns class
  }
}

const createNotes = document.getElementById('create'); 

createNotes.addEventListener('click', function(event) {
  event.preventDefault(); // prevent the default behavior of the link

  // Send an AJAX request to the Flask route
  fetch('/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response from the server
    if (data.status === 'success') {
      location.reload();
    } else {
      console.error('Error inserting data');
    }
  })
  .catch(error => {
    console.error('Error sending request:', error);
  });
});

const deleteNotes = document.querySelectorAll('.delete-btn');

deleteNotes.forEach(button => {
  button.addEventListener('click', function(event) {
    event.preventDefault(); // prevent the default behavior of the link
    const noteId = button.getAttribute('data-id');
    
    // Send an AJAX request to the Flask route
    fetch(`/delete?id=${noteId}`, {
      method: 'DELETE',
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Remove the card from the DOM
      const card = document.querySelector(`.delete-btn[data-id="${noteId}"]`).parentNode;
      card.remove();
    })
    .catch(error => {
      console.error(error);
    });
  });
})

//script buat open popup editor
// let editContainer = document.querySelector('.edit-container');
// let popUpBox = editContainer.querySelectorAll('.editor');

// document.querySelectorAll('.container .card').forEach(card =>{
//   card.onclick = () =>{
//     editContainer.style.display = 'flex';
//     let name = card.getAttribute('data-name');
//     popUpBox.forEach(preview =>{
//       let target = preview.getAttribute('data-target');
//       if(name == target){
//         preview.classList.add('active');
//       }
//     });
//   };
// });

// popUpBox.forEach(close =>{
//   close.querySelector('.close').onclick = () =>{
//     close.classList.remove('active');
//     editContainer.style.display = 'none';
//   };
// });

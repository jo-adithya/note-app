let sidebar = document.querySelector('.sidebar');
let sideFile = document.querySelector('.file-manager');
let closeBtn = document.querySelector('#btn');
let file = document.querySelector('#file');
let create = document.querySelector('#create');

closeBtn.addEventListener('click', () => {
  sidebar.classList.toggle('open');
  if (sideFile.classList.contains('open')) {
    sideFile.classList.toggle('open');
  }
  menuBtnChange(); //calling the function(optional)
});

file.addEventListener('click', () => {
  if (!sidebar.classList.contains('open')) {
    sidebar.classList.toggle('open');
    sideFile.classList.toggle('open');
  } else {
    sideFile.classList.toggle('open');
  }
  menuBtnChange(); //calling the function(optional)
});

create.addEventListener('click', () => {
  if (!sidebar.classList.contains('open')) {
    sidebar.classList.toggle('open');
    sideFile.classList.toggle('open');
  } else {
    sideFile.classList.toggle('open');
  }
  menuBtnChange(); //calling the function(optional)
});

// following are the code to change sidebar button(optional)
function menuBtnChange() {
  if (sidebar.classList.contains('open')) {
    closeBtn.classList.replace('bx-menu', 'bx-menu-alt-right'); //replacing the iocns class
  } else {
    closeBtn.classList.replace('bx-menu-alt-right', 'bx-menu'); //replacing the iocns class
  }
}

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


//   function showHideAnalytics() {
//   let x = document.getElementById("analytics_container");
//   if (x.style.display === 'none') {
//     x.style.display = 'block';
//   } else {
//     x.style.display = 'none'
//   }
// }

//function to show/hide analysis charts
document.addEventListener('DOMContentLoaded',function showHideAnalytics () {
  const analyticsControlButton = document.getElementById('analytics_control');
  const analyticsContainer = document.getElementById('analytics_container');

  if (analyticsControlButton) {
    analyticsControlButton.addEventListener('click', function() {
      if(analyticsContainer.style.display == 'none') {
        analyticsContainer.style.display = 'block';
      } else {
        analyticsContainer.style.display = 'none';
      }
    })
  }
})

//add_recipe_form logic
document.addEventListener('DOMContentLoaded', function () {
  // Grab the form and button
  const recipeForm = document.getElementById('recipeForm');
  const saveRecipeBtn = document.getElementById('saveRecipeBtn');

  // Add an event listener for form submission
  recipeForm.addEventListener('submit', function (e) {
      e.preventDefault();  // Prevent the default form submission

      // Create a FormData object to serialize the form data
      const formData = new FormData(recipeForm);
      const postUrl = recipeForm.getAttribute('data-post-url');

      // Send the AJAX request using the Fetch API
      fetch(postUrl, {
          method: 'POST',
          headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          },
          body: formData,
          credentials: 'same-origin' // Ensures cookies are sent with the request if the URL is on the same origin.
      })
      .then(response => {
          if (response.ok) {
              return response.json();  // Parse the JSON response
          } else {
              return response.json().then(err => { throw err });  // Handle errors
          }
      })
      .then(data => {
          // Checks if the server responded with a success status.
          if (data.status === 'success') {
            // Closes the recipe modal by hiding it.
            document.getElementById('addRecipeModal').style.display = 'none';
            // Reloads the page to reflect any changes made by the form submission.
            window.location.reload();
        }
    })
      .catch(error => {
          // Handle errors - show error message inside the modal
          document.getElementById('form-alert').innerHTML = "<div class='alert alert-danger'>There was an error: " + error.message + "</div>";
      });
  });
});


document.addEventListener('DOMContentLoaded', function() {
  // retrieves necessary HTML elements
  const openModalButton = document.getElementById('openAddRecipeBtn');
  const addRecipeModal = document.getElementById('addRecipeModal');
  const closeModalSpan = document.getElementById('closeAddRecipeModal');

  //addRecipeButton functionality
  if (openModalButton){
    openModalButton.addEventListener('click', ()=> {
      addRecipeModal.style.display = 'block';
    });
  }
    
  //closeModal functionality
  if (closeModalSpan) {
    closeModalSpan.addEventListener('click', ()=> {
      addRecipeModal.style.display = 'none';
    });
  }
  //logic to hide modal if user clicks outside of it
  window.addEventListener('click', function (e) {
    if (e.target == addRecipeModal) {
      addRecipeModal.style.display = 'none';
    }
  });
})


//update recipe modal functionality
document.addEventListener('DOMContentLoaded',function () {
  //retrieve button element that opens updateModal
  const updateButton = document.getElementById('openUpdateModalButn');
  const updateModal = document.getElementById('updateRecipeModal');
  const closeUpdateModal = document.getElementById('closeUpdateModal');

  //logic to open the modal onClick of updateButton
  if(updateButton) {
    updateButton.addEventListener('click', ()=>{
      if (updateModal) {
        updateModal.style.display = 'block';
      }
    });
  }
  //logic to close modal
  if (closeUpdateModal) {
    closeUpdateModal.addEventListener('click', ()=> {
      updateModal.style.display = 'none';
    });
  }
    //logic to hide modal if user clicks outside of it
    window.addEventListener('click', (e)=> {
      if (e.target == updateModal) {
        updateModal.style.display = 'none';
      }
    });
  
})


//update recipe form logic
document.addEventListener('DOMContentLoaded', function () {
  const updateRecipeForm = document.getElementById('updateRecipeForm');

  updateRecipeForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(updateRecipeForm);

    fetch(updateRecipeForm.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: formData
    })
    .then(response => {
      if(response.ok) {
        return response.json();
      } else {
        return response.json().then(err => { throw err})
      }
    })
    .then(data => {
      if (data.status === 'success') {
        // Closes the recipe modal by hiding it.
        document.getElementById('updateRecipeModal').style.display = 'none';
        // Reloads the page to reflect any changes made by the form submission.
        window.location.reload();
    }
    });
  });
});


//deleting the recipe functionality
document.addEventListener('DOMContentLoaded', function () {
  //retrieving CSRF token necessary for POST requests
  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Checks if the current cookie is the one we're looking for.
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // exit the looop once cookie is found
            }
        }
    }
    return cookieValue; // Return the found cookie value or null if not found.
  }

  //retrieve necessary DOM elements
  const deleteButton = document.getElementById('deleteRecipeButton');
  const deleteModal = document.getElementById('delete_recipe_modal');
  const closeDeleteModal = document.getElementById('closeDeleteModal');
  const confirmDeleteButton = document.getElementById('confirmDeleteButton');
  
  //display delete confirmation modal when "delete" button is clicked
  if(deleteButton) {
    deleteButton.addEventListener('click', ()=> {
      deleteModal.style.display = 'block';
    });
  }

  //close delete confirmation modal when "close" button is clicked
  if (closeDeleteModal) {
    closeDeleteModal.addEventListener('click', ()=> {
      deleteModal.style.display = 'none';
    });
  }

  //logic to hide modal if user clicks outside of it
  if (deleteModal){
    window.addEventListener('click', (e) => {
      if (e.target == deleteModal) {
        deleteModal.style.display ='none';
      }
    });
  }

  //confirm deletion
  if (confirmDeleteButton) {
    confirmDeleteButton.addEventListener('click', function () {
      const recipeId = deleteButton.dataset.recipeId; // Retrieve the recipe ID from the data-attribute

      if (confirmDeleteButton) {
        // Make a POST request to the server to delete the recipe
        fetch(`/delete/${recipeId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
          },
          credentials: 'include' // Ensure credentials such as cookies are included with the request
        })
        .then(response => response.json()) // Parse the JSON response from the server
        .then(data => {
          if (data.status === 'success') {
            // Notify the user of successful deletion and redirect to the list page
            alert('Recipe successfully deleted.');
            window.location.href = "/list/";
          } else {
            // Alert the user of an error based on the message from the server
            alert(`Error: ${data.message}`);
          }
        }).catch(error => {
          // Log and alert the user of any errors that occurred during the fetch operation
          console.error('Error:', error);
          alert(`An error occurred: ${error}`);
        });
      } else {
        alert("You must click button to confirm.");
      }
    });
  }
})


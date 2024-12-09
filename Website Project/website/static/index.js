function deleteNote(noteId) {
    fetch("/delete-entry", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ entryId: noteId }),
    })
    .then((response) => {
      if (response.ok){
        window.location.href = "/";
      } else {
        return response.json().then((data) => {
          alert(data.error || 'An error occurred while deleting the entry');
      });

    }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Failed to delete the entry, try again');
});
}
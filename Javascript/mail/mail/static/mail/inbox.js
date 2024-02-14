document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //This deals with the submision of the email 
  document.querySelector("#compose-form").addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#detailed-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}
function view_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#detailed-email').style.display = 'block';


      if (!email.archived) {
        document.querySelector('#detailed-email').innerHTML = `
      <ul class="list-group">
      <li class="list-group-item"><h5>From:</h5>${email.sender} </li>
      <li class="list-group-item"><h5>To:</h5>${email.recipients} </li>
      <li class="list-group-item"><h6>Subject:</h6>${email.subject} </li>
      <li class="list-group-item"><h6>Timestamp:</h6>${email.timestamp} </li>
      <li class="list-group-item">${email.body} </li>
      
      
      </ul>
      <button id="reply-button">Reply</button>
      </ul>
      <button id="archive-button">Archive</button>
      `
      } else {
        document.querySelector('#detailed-email').innerHTML = `
      <ul class="list-group">
      <li class="list-group-item"><h5>From:</h5>${email.sender} </li>
      <li class="list-group-item"><h5>To:</h5>${email.recipients} </li>
      <li class="list-group-item"><h6>Subject:</h6>${email.subject} </li>
      <li class="list-group-item"><h6>Timestamp:</h6>${email.timestamp} </li>
      <li class="list-group-item">${email.body} </li>
      
      
      </ul>
      <button id="reply-button">Reply</button>
      </ul>
      <button id="archive-button">Unarchive</button>
      `
      };

      const archiveButton = document.querySelector('#archive-button');

      //Add a click event listener to the archive button
      archiveButton.addEventListener('click', function () {


        archive_email(id);
      });



      const data = {
        "read": true
      };

      //Send a PUT request to /emails/<email_id> with the data object as the request body
      fetch(`/emails/${id}`, {
        method: "PUT",
        body: JSON.stringify(data)
      })


      const replyButton = document.querySelector('#reply-button');
      replyButton.addEventListener('click', function () {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if(subject.split(' ',1)[0] != "Re:"){
          subject= "Re: " + email.subject;
        }
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

      });

    });
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detailed-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  //Get the emails for that mailbox and user
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);
      // Loop through the emails
      emails.forEach(singleEmail => {
        //Create div for each email
        console.log(singleEmail);
        const newEmail = document.createElement('div');
        newEmail.className = "list-group-item";
        newEmail.innerHTML =
          `<h6>sender: ${singleEmail.sender}</h6>
 <h5>subject: ${singleEmail.subject}</h5>
<p>${singleEmail.timestamp}</p>`;

        if (singleEmail.read) {
          //If the email is read, use a light gray color
          newEmail.style.backgroundColor = "#f0f0f0";
        } else {
          //If the email is unread, use a white color
          newEmail.style.backgroundColor = "#ffffff";
        }


        newEmail.addEventListener('click', function () {
          view_email(singleEmail.id)
        });
        document.querySelector('#emails-view').append(newEmail);

      })


    });

}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  const data = {
    "recipients": recipients,
    "subject": subject,
    "body": body
  }

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify(data),

  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    })
}

function archive_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {


      const data = {
        "archived": !email.archived
      };
      //Send a PUT request to update the email
      fetch(`/emails/${id}`, {
        method: "PUT",
        body: JSON.stringify(data)
      })
        .then(() => {
          //Do something after the request is successful
          console.log("Email archived status changed");
          //Reload the mailbox view
          load_mailbox('inbox');
        });
    });
}








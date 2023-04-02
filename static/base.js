function getLink()
  {
    text = "";
    text = document.getElementById("csong").value;
    linkText = "<a href='https://mixqueue.sarahlong4.repl.co/rec?song=" + text + "' class='btn'>Print Song</a>";
    document.getElementById("linkGet").innerHTML = linkText;
  }

function getSong()
  {
    var rec = document.getElementById("rec").innerHTML;
    var song = document.getElementById("song").innerHTML;
    // If no song is entered
    if (rec == "")
    {
      alert("Please Enter a song.");
    }
    else
    {
      //Removes whitespace
      let count = 0;
      if (rec[0] == " ")
      {
        for (let i = 0; i < rec.length; i++) 
        {
          if (rec[i] == " ")  
          {
            count++;
          }
        }
      }
  
      if (count != 0)
      {
        // To account for the cluster number and extra space
        rec = rec.slice(count+2)
      }
      
      document.getElementById("csong").value = song;
      document.getElementById("nsong").value = rec;
    }
  }
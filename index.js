const xhr = new XMLHttpRequest();
xhr.open('GET', 'out/files.json');
xhr.responseType = 'application/json';
xhr.onload = () => {
  const files = JSON.parse(xhr.response);
  files.forEach(f => {
    document.body.innerHTML += '<div><img src="' + f + '" class="graph" /></div>';
  });
  document.body.innerHTML += '<p>Data from the New York Times covid tracking project. Updated twice daily.<p>'
}
xhr.send();
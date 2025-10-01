const fs = require('fs');

const readmePath = './README.md';
const skillsData = fs.readJsonSync('./skills.json');

let readme = fs.readFileSync(readmePath, 'utf-8');

// Build the Skills Table
let table = `<table style="border-collapse: collapse; border-radius: 12px; overflow: hidden; width: 100%;">
<tr><th>Language / Tool</th><th>Proficiency</th><th>Hours Spent</th></tr>`;

skillsData.skills.forEach(skill => {
    table += `<tr>
<td><b>${skill.name}</b></td>
<td>
<div style="background:#ddd; border-radius:8px; width:100%; overflow:hidden;">
<div style="width:${skill.proficiency}%; background:#3776AB; padding:5px 0; border-radius:8px; color:white; text-align:center; animation: fillBar 2s ease-in-out;">${skill.proficiency}%</div>
</div>
</td>
<td>${skill.hours}+ hrs</td>
</tr>`;
});

table += '</table>\n<style>@keyframes fillBar {0%{width:0;}100%{width:inherit;}}</style>';

// Replace existing Skills Overview section
readme = readme.replace(/## 🛠 Skills Overview[\s\S]*?<style>[\s\S]*?<\/style>/, `## 🛠 Skills Overview\n\n${table}`);

fs.writeFileSync(readmePath, readme);
console.log('README updated with latest skills!');

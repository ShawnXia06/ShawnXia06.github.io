# Shawn Xia: personal site

A one-page site with a poker theme. There's no build step: open `index.html` in a browser to see it.

```
index.html              the whole site
favicon.svg             tab icon (plus favicon-32.png and apple-touch-icon.png)
photos/                 your photos go here
tools/process_photos.py gives every photo the same edit (optional)
```

## Edit your content

Open `index.html` in VS Code and find the block that starts with
`YOUR CONTENT — edit everything in this block`. Everything you'd want to change
is in there:

| What | Where in the block |
|---|---|
| Name, subtitle, the one-line takeaway | top of `SITE` |
| About text, fact pills, the two face-up cards | `about`, `facts`, `holeCards` |
| Jobs | `jobs` |
| Campus involvement (the seat chart) | `involvement` |
| Projects | `projects` |
| Skills, certifications, coursework | `skills`, `certifications`, `coursework` |
| Map places and zoom buttons | `places`, `presets` |
| Hobbies and their photos | `hobbies` |
| Email, LinkedIn, GitHub | `contact` |

To add an entry, copy an existing `{ ... }` block, paste it right after (put a comma between the two blocks), and change the text.

Any text containing `TODO` shows on the page with a dashed gold underline, so nothing unfinished can slip through. Search the file for `TODO` before you publish.

## Add photos

1. Put the photo in `photos/`. Use a simple name with no spaces, like `photos/rubad-tryouts.jpg`.
2. Reference it where it belongs:
   - headshot: `headshot: { src: "photos/headshot.jpg", caption: "..." }`
   - hobby: add `{ src: "photos/rubad-tryouts.jpg", caption: "tryouts" }` to that hobby's `photos` list
3. A photo with `src: ""` shows a "photo coming soon" frame.

To give a batch the site's look (white balance, warm tone, resized to 1400 px, around 250 KB, location and camera data removed):

```
pip install pillow
python3 tools/process_photos.py ~/Desktop/new-photos photos/
```

This also writes `photos/_before_after.jpg` so you can compare the results. Delete that file afterward.

**Photos of friends and family will be public.** Ask before you post them.

## Add a map place

1. In Google Maps, right-click the spot and click the two numbers at the top of the menu. That copies them, e.g. `40.7128, -74.0060`.
2. Add a line to `homes`, `visited` or `want`:

```js
{ name: "Boston, MA", lat: 42.36, lng: -71.06, note: "" },
```

The site works out each place's state or country by itself. That fills in the totals, the shading and the groups in the list under the map. For a home, use the town's general area, never your street.

The map draws countries at a simplified scale, so a dot in a very small country (Singapore, Monaco) may not be detected. Add `country: "Singapore"` to that place to fix it.

## Publish on Netlify with your own domain

1. **Create a Netlify account** at app.netlify.com (the free plan is enough). Sign up with GitHub or email.
2. **Deploy:** click **Add new site → Deploy manually**, then drag the whole site folder (or the zip) onto the page. A minute later you'll have a live URL like `random-name.netlify.app`.
3. **Rename it:** go to **Site configuration → Change site name**, e.g. `shawnxia.netlify.app`.
4. **Get a domain.** Pick one of these:
   - **Through Netlify** (easiest): go to **Domain management → Add a domain → Register a new domain**. DNS and HTTPS are set up for you, so skip to step 6.
   - **Through Porkbun or Namecheap** (often cheaper): buy `shawnxia.com` and make sure WHOIS privacy is on. Porkbun includes it free, and on Namecheap it's called "Domain Privacy".
5. **Point the domain at Netlify** (only if you bought it elsewhere):
   - In Netlify, go to **Domain management → Add a domain you already own**, type it in and confirm.
   - The easiest option is **Set up Netlify DNS**. Netlify shows four nameservers like `dns1.p01.nsone.net`. At Porkbun or Namecheap, find **Nameservers**, switch to custom, and paste all four in.
   - The other option is to keep your registrar's DNS and add two records: an `A` record for `@` pointing to `75.2.60.5`, and a `CNAME` for `www` pointing to `yoursite.netlify.app`.
   - DNS can take anywhere from a few minutes to 24 hours.
6. **HTTPS:** go to **Domain management → HTTPS**. Netlify issues a free Let's Encrypt certificate once DNS is live. Click **Verify DNS configuration** if it hasn't started on its own.
7. **Update the site later:** go to **Deploys**, then drag the updated folder onto the deploy drop zone. The old version stays in the list in case you need to roll back.

GitHub Pages also works: upload the folder's contents to a `username.github.io` repository and turn on Pages under **Settings → Pages**.

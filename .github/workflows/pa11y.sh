#! /bin/bash
set +e

reports_dir="reports/pa11y"
site_url="http://127.0.0.1:8000"
exit_code=0

mkdocs build
mkdir -p "$reports_dir"

printf -- 'scanning: /\n'
./node_modules/.bin/pa11y "$site_url" || exit_code=2

for file in $(xq '.urlset.url[].loc' site/sitemap.xml -r | sed -r 's!https://jrnl.sh/(.*?)/$!\1!'); do
  printf -- 'scanning: /%s\n' "$file"
  ./node_modules/.bin/pa11y "$site_url/$file" || exit_code=2
done

exit $exit_code

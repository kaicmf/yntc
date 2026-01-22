source "https://rubygems.org"
# Hello! This is the default Gemfile for new Jekyll sites. You may edit this file to add future gems here.
#
# When you want to use a different Jekyll version or install additional gems, add them to this file
# and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is being executed.
# Happy Jekylling!

# About the jekyll gem, see: https://rubygems.org/gems/jekyll/
gem "jekyll", "~> 4.3.0"

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
  gem "jekyll-paginate", "~> 1.1"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", "~> 2.0"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
# gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` to `v0.6.x` on JRuby. If you upgrade to a newer version of Rakefile, you may need to tweak this constraint.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

# Theme - Chirpy
gem "jekyll-theme-chirpy", "~> 6.0"

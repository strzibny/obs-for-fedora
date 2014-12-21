# This spec tries to follow upstream packaging

# Define OBS install directories
%global obslibdir /usr/lib/obs
%global obsserverdir %{obslibdir}/server
%global obswwwdir /srv/www/obs
%global obsapidir %{obswwwdir}/api
# Define Apache user.group
%global apache_user apache
%global apache_group apache
# Define SELinux
%global selinux_variants targeted
%global modulename obspol

Name:           obs-server
Summary:        The Open Build Service Server Component
License:        GPLv2 && GPLv3
Group:          Applications/System

%global stable_version 2.5.50

# Git release 3647e3
Version:        2.5.50.git3647e3
Release:        4
Url:            https://github.com/openSUSE/open-build-service
# Clone upstream repo and fedora-obs repo
#   ./prepare-obs-sources
Source0:        open-build-service-%{stable_version}.tar.gz
# systemd files for OBS
Source1:        open-build-service-%{stable_version}-systemd.tar.gz
# From fedora-repo since it differs from upstream a bit
Source2:        find-requires.sh
# Static assets for bento theme
#   http://static.opensuse.org/themes/bento/css/images/
Source3:        bento-images.tar.gz
# SELinux policies
Source4:        open-build-service-selinux.tar.gz

Requires:       build >= 20140710
Requires:       obs-productconverter >= %version
Requires:       obs-worker
Requires:       perl-BSSolv >= 0.01
# Required by source server
Requires:       diffutils
Requires:       patch
# Require the createrepo and python-yum versions
Requires:       %(/bin/bash -c 'rpm -q --qf "%%{name} = %%{version}-%%{release}" createrepo')
# Fedora python-yum
Requires:       %(/bin/bash -c 'rpm -q --qf "%%{name} = %%{version}-%%{release}" yum')
Requires:       perl-Compress-Zlib
Requires:       perl-File-Sync >= 0.10
Requires:       perl-JSON-XS
Requires:       perl-Net-SSLeay
Requires:       perl-Socket-MsgHdr
Requires:       perl-XML-Parser
Requires:       perl-XML-Simple
BuildRequires:  python-devel
BuildRequires:  systemd
# This needs to be in sync with the RAILS_GEM_VERSION
# specified in the config/environment.rb of the various
# applications.
BuildRequires:  build >= 20140710
BuildRequires:  perl-BSSolv
BuildRequires:  perl-Compress-Zlib
BuildRequires:  perl-File-Sync >= 0.10
BuildRequires:  perl-JSON-XS
BuildRequires:  perl-Net-SSLeay
BuildRequires:  perl-Socket-MsgHdr
BuildRequires:  perl-TimeDate
BuildRequires:  perl-XML-Parser
BuildRequires:  perl-XML-Simple
BuildRequires:  procps
BuildRequires:  memcached
BuildArch:      noarch

%description
The Open Build Service (OBS) backend is used to store all
sources and binaries. It also calculates the need for new
build jobs and distributes them.

%package -n obs-worker
Summary:        The Open Build Service Build Host Component
Group:          Applications/System
Requires:       cpio
Requires:       curl
Requires:       perl-Compress-Zlib
Requires:       perl-TimeDate
Requires:       perl-XML-Parser
Requires:       screen
Requires:       openslp
# For build script
Requires:       psmisc
# For runlevel script:
Requires:       curl
Requires:       bash
Requires:       binutils
# bsdtar on Fedora should be provided by libarchive
Requires:       libarchive
Requires:       util-linux >= 2.16

%description -n obs-worker
This is the OBS build host which needs to be installed on each
machine building packages in this OBS installation. Install it
alongside obs-server to run a local playground test installation.

%package -n obs-api
Summary:        The Open Build Service API and WEBUI
Group:          Applications/System

# For session data
Requires:       memcached
Conflicts:      memcached < 1.4
Requires:       openssl-perl
Requires:       httpd
Requires:       mariadb
Requires:       mariadb-server
Requires:       ruby(release)
Requires:       rubygem(bundler)
Requires:       rubygem(passenger)
# Apache modules used by OBS config
# XForward is not in Fedora and therefore not used
Requires:       mod_ssl
Requires:       mod_passenger
# For rebuild_time
Requires:       perl(GD)
# Needed for fulltext searching
# Fedora 21 has version 2.1.5
Requires:       sphinx >= 2.1.5

BuildRequires:  hardlink
BuildRequires:  rubygem(bundler)
BuildRequires:  createrepo
BuildRequires:  curl
BuildRequires:  memcached >= 1.4
BuildRequires:  mariadb-server

# Rails app gem depencencies
Requires: rubygem(rake)
Requires: rubygem(i18n) >= 0.6.9
Requires: rubygem(i18n) < 0.7
Requires: rubygem(json) >= 1.8.1
Requires: rubygem(minitest)
Requires: rubygem(thread_safe) >= 0.3.3
Requires: rubygem(tzinfo) >= 1.1.0
Requires: rubygem(activesupport) >= 4.1.0
Requires: rubygem(builder) >= 3.2.2
Requires: rubygem(erubis) >= 2.7.0
Requires: rubygem(actionview) >= 4.1.0
Requires: rubygem(rack) >= 1.5.2
Requires: rubygem(rack-test) >= 0.6.2
Requires: rubygem(actionpack) >= 4.1.0
Requires: rubygem(mime-types) >= 1.25.1
Requires: rubygem(polyglot) >= 0.3.4
Requires: rubygem(treetop)
Requires: rubygem(mail) >= 2.5.4
Requires: rubygem(actionmailer) >= 4.1.0
Requires: rubygem(activemodel) >= 4.1.0
Requires: rubygem(arel) >= 5.0.0
Requires: rubygem(activerecord) >= 4.1.0
Requires: rubygem(acts_as_list) >= 0.4.0
Requires: rubygem(addressable) >= 2.3.6
Requires: rubygem(mini_portile) >= 0.6.0
Requires: rubygem(nokogiri) >= 1.6.3
Requires: rubygem(nokogiri) < 1.7
Requires: rubygem(xpath) >= 2.0.0
Requires: rubygem(capybara)
Requires: rubygem(capybara_minitest_spec)
Requires: rubygem(chunky_png)
Requires: rubygem(ci_reporter)
Requires: rubygem(cliver)
Requires: rubygem(clockwork) >= 0.7.0
Requires: rubygem(cocoon) >= 1.2.6
Requires: rubygem(thor)
Requires: rubygem(railties) >= 4.1.0
Requires: rubygem(codemirror-rails) >= 4.2
Requires: rubygem(coderay) >= 1.1.0
Requires: rubygem(safe_yaml) >= 1.0.3
Requires: rubygem(crack) >= 0.4.2
Requires: rubygem(cssmin) >= 1.0.2
Requires: rubygem(daemons) >= 1.1.9
Requires: rubygem(dalli) >= 2.7.2
Requires: rubygem(database_cleaner)
Requires: rubygem(delayed_job) >= 4.0.1
Requires: rubygem(delayed_job_active_record) >= 4.0.1
Requires: rubygem(docile) >= 1.1.3
Requires: rubygem(escape_utils)
Requires: rubygem(execjs) >= 2.0.2
Requires: rubygem(faker)
Requires: rubygem(sexp_processor) >= 4.4.3
Requires: rubygem(ruby_parser) >= 3.5.0
Requires: rubygem(flog) >= 4.1.0
Requires: rubygem(font-awesome-rails)
Requires: rubygem(tilt) >= 1.4.1
Requires: rubygem(haml) >= 4.0.5
Requires: rubygem(hike) >= 1.2.3
Requires: rubygem(hoptoad_notifier) >= 2.3
Requires: rubygem(innertube) >= 1.1.0
#Requires: rubygem(joiner)
Requires: rubygem(jquery-rails)
Requires: rubygem(jquery-datatables-rails)
Requires: rubygem(jquery-ui-rails)
Requires: rubygem(kaminari) >= 0.15.1
Requires: rubygem(kgio)
Requires: rubygem(metaclass) >= 0.0.4
Requires: rubygem(method_source)
Requires: rubygem(middleware) >= 0.1.0
Requires: rubygem(mocha) >= 0.13.0
Requires: rubygem(multi_json)
Requires: rubygem(mysql2)
Requires: rubygem(pkg-config) >= 1.1.5
Requires: rubygem(websocket-driver) >= 0.3.3
Requires: rubygem(poltergeist) >= 1.4.0
Requires: rubygem(slop) >= 3.5.0
#Requires: rubygem(pry) >= 0.9.12.6
Requires: rubygem(pundit)
#Requires: rubygem(rack-mini-profiler) >= 0.9.1
Requires: rubygem(sprockets) >= 2.10.1
Requires: rubygem(sprockets-rails) >= 2.1.0
Requires: rubygem(rails) >= 4.1.0
Requires: rubygem(rails_tokeninput)
Requires: rubygem(raindrops)
Requires: rubygem(rdoc) >= 4.1.0
Requires: rubygem(redcarpet)
Requires: rubygem(riddle) >= 1.5.11
Requires: rubygem(ruby-ldap)
Requires: rubygem(sass) >= 3.2.19
Requires: rubygem(sass-rails) >= 4.0.3
Requires: rubygem(sass-rails) < 4.1
Requires: rubygem(simplecov-html)
Requires: rubygem(simplecov)
Requires: rubygem(sprite-factory) >= 1.5.2
Requires: rubygem(thinking-sphinx)
Requires: rubygem(timecop) >= 0.7.1
Requires: rubygem(uglifier) >= 1.2.2
#Requires: rubygem(unicorn) >= 4.8.3
#Requires: rubygem(unicorn-rails) >= 2.1.1
Requires: rubygem(webmock)
Requires: rubygem(xmlhash) >= 1.3.6
Requires: rubygem(yajl-ruby)

BuildRequires: rubygem(rake)
#BuildRequires: rubygem(rake) >= 10.3.2
#BuildRequires: rubygem(rake) < 10.4
BuildRequires: rubygem(i18n) >= 0.6.9
BuildRequires: rubygem(i18n) < 0.7
BuildRequires: rubygem(json) >= 1.8.1
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(thread_safe) >= 0.3.3
BuildRequires: rubygem(tzinfo) >= 1.1.0
BuildRequires: rubygem(activesupport) >= 4.1.0
BuildRequires: rubygem(builder) >= 3.2.2
BuildRequires: rubygem(erubis) >= 2.7.0
BuildRequires: rubygem(actionview) >= 4.1.0
BuildRequires: rubygem(rack) >= 1.5.2
BuildRequires: rubygem(rack-test) >= 0.6.2
BuildRequires: rubygem(actionpack) >= 4.1.0
BuildRequires: rubygem(mime-types) >= 1.25.1
BuildRequires: rubygem(polyglot) >= 0.3.4
BuildRequires: rubygem(treetop)
#BuildRequires: rubygem(treetop) >= 1.4.15
BuildRequires: rubygem(mail) >= 2.5.4
BuildRequires: rubygem(actionmailer) >= 4.1.0
BuildRequires: rubygem(activemodel) >= 4.1.0
BuildRequires: rubygem(arel) >= 5.0.0
BuildRequires: rubygem(activerecord) >= 4.1.0
BuildRequires: rubygem(acts_as_list) >= 0.4.0
BuildRequires: rubygem(addressable) >= 2.3.6
BuildRequires: rubygem(mini_portile) >= 0.6.0
BuildRequires: rubygem(nokogiri) >= 1.6.3
BuildRequires: rubygem(xpath) >= 2.0.0
BuildRequires: rubygem(capybara)
BuildRequires: rubygem(capybara_minitest_spec)
BuildRequires: rubygem(chunky_png)
BuildRequires: rubygem(ci_reporter)
BuildRequires: rubygem(cliver)
BuildRequires: rubygem(clockwork) >= 0.7.0
BuildRequires: rubygem(cocoon) >= 1.2.6
BuildRequires: rubygem(thor)
#BuildRequires: rubygem(thor) >= 0.19.1
BuildRequires: rubygem(railties) >= 4.1.0
BuildRequires: rubygem(codemirror-rails) >= 4.2
BuildRequires: rubygem(coderay) >= 1.1.0
BuildRequires: rubygem(safe_yaml) >= 1.0.3
BuildRequires: rubygem(crack) >= 0.4.2
BuildRequires: rubygem(cssmin) >= 1.0.2
BuildRequires: rubygem(daemons) >= 1.1.9
BuildRequires: rubygem(dalli) >= 2.7.2
BuildRequires: rubygem(database_cleaner)
BuildRequires: rubygem(delayed_job) >= 4.0.1
BuildRequires: rubygem(delayed_job_active_record) >= 4.0.1
BuildRequires: rubygem(docile) >= 1.1.3
BuildRequires: rubygem(escape_utils)
BuildRequires: rubygem(execjs) >= 2.0.2
BuildRequires: rubygem(faker)
BuildRequires: rubygem(sexp_processor) >= 4.4.3
BuildRequires: rubygem(ruby_parser) >= 3.5.0
BuildRequires: rubygem(flog) >= 4.1.0
BuildRequires: rubygem(font-awesome-rails)
BuildRequires: rubygem(tilt) >= 1.4.1
BuildRequires: rubygem(haml) >= 4.0.5
BuildRequires: rubygem(hike) >= 1.2.3
BuildRequires: rubygem(hoptoad_notifier) >= 2.3
#BuildRequires: rubygem(hoptoad_notifier) < 2.4
BuildRequires: rubygem(innertube) >= 1.1.0
#BuildRequires: rubygem(joiner)
BuildRequires: rubygem(jquery-rails)
BuildRequires: rubygem(jquery-datatables-rails)
BuildRequires: rubygem(jquery-ui-rails)
BuildRequires: rubygem(kaminari) >= 0.15.1
BuildRequires: rubygem(kgio)
BuildRequires: rubygem(metaclass) >= 0.0.4
BuildRequires: rubygem(method_source)
BuildRequires: rubygem(middleware) >= 0.1.0
BuildRequires: rubygem(mocha) >= 0.13.0
BuildRequires: rubygem(multi_json)
BuildRequires: rubygem(mysql2)
BuildRequires: rubygem(pkg-config) >= 1.1.5
BuildRequires: rubygem(websocket-driver) >= 0.3.3
BuildRequires: rubygem(poltergeist) >= 1.4.0
BuildRequires: rubygem(slop) >= 3.5.0
#BuildRequires: rubygem(pry) >= 0.9.12.6
BuildRequires: rubygem(pundit)
#BuildRequires: rubygem(rack-mini-profiler) >= 0.9.1
BuildRequires: rubygem(sprockets) >= 2.10.1
BuildRequires: rubygem(sprockets-rails) >= 2.1.0
BuildRequires: rubygem(rails) >= 4.1.0
BuildRequires: rubygem(rails_tokeninput)
BuildRequires: rubygem(raindrops)
BuildRequires: rubygem(rdoc) >= 4.1.0
BuildRequires: rubygem(redcarpet)
#BuildRequires: rubygem(redcarpet) >= 3.1.2
BuildRequires: rubygem(riddle) >= 1.5.11
BuildRequires: rubygem(ruby-ldap)
BuildRequires: rubygem(sass) >= 3.2.19
BuildRequires: rubygem(sass-rails) >= 4.0.3
BuildRequires: rubygem(sass-rails) < 4.1
BuildRequires: rubygem(simplecov-html)
BuildRequires: rubygem(simplecov)
BuildRequires: rubygem(sprite-factory) >= 1.5.2
BuildRequires: rubygem(thinking-sphinx)
BuildRequires: rubygem(timecop) >= 0.7.1
BuildRequires: rubygem(uglifier) >= 1.2.2
#BuildRequires: rubygem(unicorn) >= 4.8.3
#BuildRequires: rubygem(unicorn-rails) >= 2.1.1
BuildRequires: rubygem(webmock)
BuildRequires: rubygem(xmlhash) >= 1.3.6
BuildRequires: rubygem(yajl-ruby)

# JavaScript runtime
BuildRequires: nodejs

%description -n obs-api
This is the API server instance, and the web client for the OBS.


%package -n obs-selinux
Summary:        The Open Build Service SELinux policies
Group:          Applications/System
# SELinux
%if "%{_selinux_policy_version}" != ""
Requires:       selinux-policy >= %{_selinux_policy_version}
%endif
Requires(post):   /usr/sbin/semodule, /sbin/restorecon, /sbin/semanage
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /sbin/semanage
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy-devel
BuildRequires:  /usr/share/selinux/devel/policyhelp


%description -n obs-selinux
SELinux policy files and rules.


%package -n obs-devel
Summary:        The Open Build Service API and WEBUI Testsuite
Group:          Applications/System
Requires:       obs-api = %{version}-%{release}

%description -n obs-devel
Install to track dependencies for git.

%package -n obs-source_service
Summary:        The Open Build Service Source Service Daemon
Group:          Applications/System

%description -n obs-source_service
The OBS source service is a component to modify submitted sources
on the server side. This may include source checkout, spec file
generation, gpg validation, quality checks and other stuff.

This component is optional and not required to run the service.

%package -n obs-productconverter
Summary:        The Open Build Service Product Definition Utility
Group:          Applications/System
Requires:       obs-server

%description -n obs-productconverter
bs_productconvert is a utility to create Kiwi- and Spec- files from
a product definition.

%package -n obs-utils
Summary:        The Open Build Service Utilities
Group:          Applications/System
Requires:       build
Requires:       osc
Requires:       ruby(release)

%description -n obs-utils
obs_project_update is a tool to copy a packages of a project from one obs to another.

%prep
%setup -q -n open-build-service-%stable_version

# Extract systemd files
mkdir systemd
tar -xf %{SOURCE1} -C systemd

# Extract SELinux files
mkdir selinux
tar -xf %{SOURCE4} -C selinux

# Drop build script, the installed one is required
rm -rf src/build
find . -name .git\* -o -name Capfile -o -name deploy.rb | xargs rm -rf

%build
pushd src/api
# Remove development section from Gemfile to avoid Bundler issues
# and adjust dependencies
rm Gemfile.lock
#sed -i -e '88,98d' Gemfile
sed -i -e '57,98d' Gemfile
#sed -i -e "s|gem 'nokogiri', '~>1.6.3'|gem 'nokogiri', '~> 1.6.4'|" Gemfile
sed -i -e "s|gem 'thinking-sphinx', '> 3.1'|gem 'thinking-sphinx', '>= 3.1'|" Gemfile

# For jquery-ui-rails 5.0.x
sed -i -e 's|jquery\.ui\.|jquery-ui/|' app/assets/javascripts/webui/application.js 

# bundle with RPM installed RubyGems
bundle --local

# Static assets for bento theme
tar -xf %{SOURCE3} -C app/assets/images/images
popd

# Generate documentation for API
pushd docs/api/api
make apidocs
popd

# Make sure Build is on path (in @INC)
pushd src/backend
sed -i "55iuse lib '/usr/lib/build'\;" ./bs_srcserver
popd

# Make SELinux policy
pushd selinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv ./%{modulename}.pp ./%{modulename}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
popd

%install
# Install SELinux files
pushd selinux
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 %{modulename}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
done
popd

/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux

# Install all distribution files
pushd dist

# Fedora use different user:group for apache
find -type f | xargs sed -i '1,$s/wwwrun\(.*\)www/apache\1apache/g'
find -type f | xargs sed -i '1,$s/user wwwrun/user apache/g'
find -type f | xargs sed -i '1,$s/group www/group apache/g'

# Configure Apache
# vhosts.d conf.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 0644 obs-apache24.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/obs.conf

# Install overview page template
mkdir -p %{buildroot}%{obswwwdir}/overview
install -m 0644 overview.html.TEMPLATE %{buildroot}%{obswwwdir}/overview/

# Install OBS mirror script and OBS copy script
install -d -m 755 %{buildroot}%{_sbindir}/
install -m 0755 obs_project_update %{buildroot}%{_sbindir}/

# Install runlevel scripts
install -d -m 755 %{buildroot}%{_sysconfdir}/init.d/
popd

# Adjust Apache configuration file
# XForward is not in Fedora, disable
sed -i -e "s/XForward on/#XForward on/g" %{buildroot}%{_sysconfdir}/httpd/conf.d/obs.conf
# Fix Apache log path
sed -i -e "s/var\/log\/apache2/var\/log\/httpd/g" %{buildroot}%{_sysconfdir}/httpd/conf.d/obs.conf

# Put systemd files in place
mkdir -p %{buildroot}%{_unitdir}
for i in obssrcserver obsrepserver obsscheduler obsworker obspublisher obsdispatcher \
         obssigner obswarden obsservice obsstoragesetup obsapidelayed obsapisetup
do
  install -m 0755 systemd/bin/$i %{buildroot}%{_sbindir}/$i
  install -m 0644 systemd/$i.service %{buildroot}%{_unitdir}/$i.service
done

pushd dist

# Install logrotate
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d/
for i in obs-api obs-server ; do
  install -m 0644 ${i}.logrotate \
           %{buildroot}%{_sysconfdir}/logrotate.d/$i
done

# Let's stick with upstream for now and put the conf file into %{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
install -m 0644 sysconfig.obs-server %{buildroot}%{_sysconfdir}/sysconfig/obs-server

# For service discovery with SLP
SLP_DIR=%{buildroot}%{_sysconfdir}/slp.reg.d/
install -d -m 755  $SLP_DIR
install -m 644 obs.source_server.reg $SLP_DIR/
install -m 644 obs.repo_server.reg $SLP_DIR/
# Create symlink for product converter
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/obs_productconvert <<EOF
#!/bin/bash
exec %{obsserverdir}/bs_productconvert "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/obs_productconvert
cat > %{buildroot}%{_sbindir}/obs_admin <<EOF
#!/bin/bash
exec %{obsserverdir}/bs_admin "\$@"
EOF
chmod 0755 %{buildroot}%{_sbindir}/obs_admin
cat > %{buildroot}%{_sbindir}/obs_serverstatus <<EOF
#!/bin/bash
exec %{obsserverdir}/bs_serverstatus "\$@"
EOF
chmod 0755 %{buildroot}%{_sbindir}/obs_serverstatus

# Install API
cd ../src
mkdir -p %{buildroot}%{obswwwdir}/
cp -a api %{buildroot}%{obsapidir}
mkdir -p %{buildroot}%{obsapidir}/log
mkdir -p %{buildroot}%{obsapidir}/tmp
touch %{buildroot}%{obsapidir}/log/production.log
touch %{buildroot}%{obsapidir}/config/production.sphinx.conf
# For running sphinx daemon
install -m 0755 -d %{buildroot}%{obsapidir}/db/sphinx{,/production}

# Install docs for API
mkdir -p %{buildroot}%{obswwwdir}/docs
cp -a ../docs/api/api %{buildroot}%{obswwwdir}/docs/
ln -sf %{obswwwdir}/docs/api %{buildroot}%{obsapidir}/public/schema
echo 'CONFIG["schema_location"] ||= File.expand_path("../docs/api/")' >> %{buildroot}%{obsapidir}/config/environment.rb

# Install backend
cd backend/
# Use external build script code as upstream does
rm -rf build
cp BSConfig.pm.template BSConfig.pm

install -d -m 755 %{buildroot}%{obsserverdir}/
ln -sf /usr/lib/build %{buildroot}%{obsserverdir}/build # just for check section, it is a %%ghost
#for i in build events info jobs log projects repos run sources trees workers; do
#  install -d -m 755 %{buildroot}/srv/obs/$i
#done
cp -a * %{buildroot}%{obsserverdir}/
rm -r   %{buildroot}%{obsserverdir}/testdata
cd ..

# These config files must not be hard linked
install -m 644 api/config/database.yml.example %{buildroot}%{obsapidir}/config/database.yml
install -m 644 api/config/options.yml.example %{buildroot}%{obsapidir}/config/options.yml
install -m 644 api/config/thinking_sphinx.yml.example %{buildroot}%{obsapidir}/config/thinking_sphinx.yml

for file in api/log/access.log api/log/backend_access.log api/log/delayed_job.log api/log/error.log api/log/lastevents.access.log; do
  touch %{buildroot}%{obswwwdir}/$file
  chmod 666 %{buildroot}%{obswwwdir}/$file
done

pushd %{buildroot}%{obsapidir}
# We need to have *something* as secret key
echo "" | sha256sum| cut -d\  -f 1 > config/secret.key
bundle exec rake --trace assets:precompile RAILS_ENV=production RAILS_GROUPS=assets
rm -rf tmp/cache/sass tmp/cache/assets config/secret.key
export BUNDLE_WITHOUT=test:assets:development
export BUNDLE_FROZEN=1
bundle config --local frozen 1
bundle config --local without test:assets:development 
# reinstall
install config/database.yml.example config/database.yml
: > log/production.log
sed -i -e 's,^api_version.*,api_version = "%version",' config/initializers/02_apiversion.rb
popd

mkdir -p %{buildroot}%{_docdir}
cat > %{buildroot}%{_docdir}/README.devel <<EOF
This package does not contain any development files. But it helps you start with 
git development - look at http://github.com/opensuse/open-build-service
EOF

rm -rf /tmp/obs.mysql.db /tmp/obs.test.mysql.socket

%pre
getent group obsrun >/dev/null || groupadd -r obsrun
getent passwd obsrun >/dev/null || \
    %{_sbindir}/useradd -r -g obsrun -d %{obslibdir} -s /sbin/nologin \
    -c "User for build service backend" obsrun
exit 0

%pre -n obs-worker
getent group obsrun >/dev/null || groupadd -r obsrun
getent passwd obsrun >/dev/null || \
    %{_sbindir}/useradd -r -g obsrun -d %{obslibdir} -s /sbin/nologin \
    -c "User for build service backend" obsrun
exit 0

%preun
#systemctl stop obssrcserver obsrepserver obsdispatcher obsscheduler obspublisher obswarden obssigner

%preun -n obs-worker
#systemctl stop obsworker

%post
#systemctl restart obssrcserver obsrepserver obsdispatcher obsscheduler obspublisher obswarden obssigner

%preun -n obs-source_service
#systemctl stop obsservice

%post -n obs-source_service
#systemctl restart obsservice

%posttrans
[ -d /srv/obs ] || install -d -o obsrun -g obsrun /srv/obs
# This changes from directory to symlink. RPM cannot handle this itself.
if [ -e %{obsserverdir}/build -a ! -L %{obsserverdir}/build ]; then
  rm -rf %{obsserverdir}/build
fi
if [ ! -e %{obsserverdir}/build ]; then
  ln -sf ../../build %{obsserverdir}/build
fi

%postun
# Cleanup OBS directories just in case
rmdir /srv/obs 2> /dev/null || :
rmdir /usr/lib/obs 2> /dev/null || :

%pre -n obs-api
getent group apache >/dev/null || groupadd -r apache
getent passwd obsapidelayed >/dev/null || \
  %{_sbindir}/useradd -r -s /bin/bash -c "User for OBS API delayed jobs" -d %{obsapidir} -g apache obsapidelayed

%post -n obs-api
if [ -e %{obswwwdir}/frontend/config/database.yml ] && [ ! -e %{obsapidir}/config/database.yml ]; then
  cp %{obswwwdir}/frontend/config/database.yml %{obsapidir}/config/database.yml
fi
for i in production.rb ; do
  if [ -e %{obswwwdir}/frontend/config/environments/$i ] && [ ! -e %{obsapidir}/config/environments/$i ]; then
    cp %{obswwwdir}/frontend/config/environments/$i %{obsapidir}/config/environments/$i
  fi
done
SECRET_KEY="%{obsapidir}/config/secret.key"
if [ ! -e "$SECRET_KEY" ]; then
  ( umask 0077; dd if=/dev/urandom bs=256 count=1 2>/dev/null |sha256sum| cut -d\  -f 1 >$SECRET_KEY )
fi
chmod 0644 $SECRET_KEY
chown root.apache $SECRET_KEY
touch %{obsapidir}/log/production.log
chown %{apache_user}:%{apache_group} %{obsapidir}/log/production.log

%post -n obs-selinux
# SELinux
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp &> /dev/null || :
done
/sbin/restorecon -vR /srv || :

# SELinux ports that are not part of loadable policy
semanage port -a -t http_port_t -p tcp 82
semanage port -a -t http_port_t -p tcp 5352

%postun -n obs-api
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
     /usr/sbin/semodule -s ${selinuxvariant} -r %{modulename} &> /dev/null || :
  done
  #[ -d %{_localstatedir}/cache/myapp ]  && \
  #  /sbin/restorecon -R /srv/obs &> /dev/null || :
fi

%files
%defattr(-,root,root)
# ReleaseNotes-* missing
%doc dist/{README.UPDATERS,README.SETUP}
%doc docs/openSUSE.org.xml
%doc README.md
%doc COPYING
%doc AUTHORS
%dir %{_sysconfdir}/slp.reg.d
%dir %{obslibdir}
%dir %{obsserverdir}
%{_sysconfdir}/logrotate.d/obs-server
# from %{_sysconfdir}/init.d
%{_sbindir}/obsdispatcher
%{_sbindir}/obspublisher
%{_sbindir}/obsrepserver
%{_sbindir}/obsscheduler
%{_sbindir}/obssrcserver
%{_sbindir}/obswarden
%{_sbindir}/obssigner
# SystemD files
%{_unitdir}/obsdispatcher.service
%{_unitdir}/obspublisher.service
%{_unitdir}/obsrepserver.service
%{_unitdir}/obsscheduler.service
%{_unitdir}/obssrcserver.service
%{_unitdir}/obswarden.service
%{_unitdir}/obssigner.service
%{_sbindir}/obs_admin
%{_sbindir}/obs_serverstatus
%{obsserverdir}/plugins
%{obsserverdir}/BSAccess.pm
%{obsserverdir}/BSBuild.pm
%{obsserverdir}/BSCando.pm
%{obsserverdir}/BSConfiguration.pm
%{obsserverdir}/BSConfig.pm.template
%{obsserverdir}/BSEvents.pm
%{obsserverdir}/BSFileDB.pm
%{obsserverdir}/BSHTTP.pm
%{obsserverdir}/BSHandoff.pm
%{obsserverdir}/BSNotify.pm
%{obsserverdir}/BSRPC.pm
%{obsserverdir}/BSServer.pm
%{obsserverdir}/BSServerEvents.pm
%{obsserverdir}/BSSrcdiff.pm
%{obsserverdir}/BSSSL.pm
%{obsserverdir}/BSStdServer.pm
%{obsserverdir}/BSUtil.pm
%{obsserverdir}/BSVerify.pm
%{obsserverdir}/BSDB.pm
%{obsserverdir}/BSDBIndex.pm
%{obsserverdir}/BSXPathKeys.pm
%{obsserverdir}/BSWatcher.pm
%{obsserverdir}/BSXML.pm
%{obsserverdir}/BSXPath.pm
%{obsserverdir}/BSProductXML.pm
%{obsserverdir}/BSKiwiXML.pm
%dir %{obsserverdir}/Meta
%{obsserverdir}/Meta.pm
%{obsserverdir}/Meta/Debmd.pm
%{obsserverdir}/Meta/Rpmmd.pm
%{obsserverdir}/Meta/Susetagsmd.pm
%{obsserverdir}/DESIGN
%doc %{obsserverdir}/License
%doc %{obsserverdir}/README
%{obsserverdir}/XML
%{obsserverdir}/bs_admin
%{obsserverdir}/bs_archivereq
%{obsserverdir}/bs_check_consistency
%{obsserverdir}/bs_getbinariesproxy
%{obsserverdir}/bs_mkarchrepo
%{obsserverdir}/bs_dispatch
%{obsserverdir}/bs_publish
%{obsserverdir}/bs_repserver
%{obsserverdir}/bs_sched
%{obsserverdir}/bs_serverstatus
%{obsserverdir}/bs_srcserver
%{obsserverdir}/bs_worker
%{obsserverdir}/bs_signer
%{obsserverdir}/bs_sshgit
%{obsserverdir}/bs_warden
%{obsserverdir}/bs_mergechanges
%{obsserverdir}/worker
%{obsserverdir}/worker-deltagen.spec
%config(noreplace) %{obsserverdir}/BSConfig.pm
%config(noreplace) %{_sysconfdir}/slp.reg.d/*
# Created via %%post since RPM fails while switching from 
# directory to symlink
%ghost %{obsserverdir}/build

%files -n obs-source_service
%defattr(-,root,root)
%{_unitdir}/obsservice.service
%{_sbindir}/obsservice
%{obsserverdir}/bs_service
%{obsserverdir}/call-service-in-lxc.sh

%files -n obs-worker
%defattr(-,root,root)
%{_sysconfdir}/sysconfig/obs-server
%{_unitdir}/obsworker.service
%{_unitdir}/obsstoragesetup.service
%{_sbindir}/obsworker
%{_sbindir}/obsstoragesetup

%files -n obs-api
%defattr(-,root,root)
# Missing ReleaseNotes-*
%doc dist/{README.UPDATERS,README.SETUP}
%doc docs/openSUSE.org.xml
%doc README.md
%doc COPYING
%doc AUTHORS
%{obswwwdir}/overview
%{obsapidir}/config/thinking_sphinx.yml.example
%config(noreplace) %{obsapidir}/config/thinking_sphinx.yml
%attr(-,%{apache_user},%{apache_group}) %config(noreplace) %{obsapidir}/config/production.sphinx.conf
%dir %{obswwwdir}
%dir %{obsapidir}
%dir %{obsapidir}/config
%{obsapidir}/config/initializers
%dir %{obsapidir}/config/environments
%dir %{obsapidir}/files
%{obsapidir}/.simplecov
%{obsapidir}/Gemfile
%{obsapidir}/Gemfile.lock
%{obsapidir}/config.ru
%{obsapidir}/config/application.rb
%{obsapidir}/config/clock.rb
%{_sysconfdir}/logrotate.d/obs-api
%{_unitdir}/obsapisetup.service
%{_unitdir}/obsapidelayed.service
%{_sbindir}/obsapisetup
%{_sbindir}/obsapidelayed
%{obsapidir}/app
%{obsapidir}/db
%{obsapidir}/files/wizardtemplate.spec
%{obsapidir}/lib
%{obsapidir}/public
%{obsapidir}/Rakefile
%{obsapidir}/script
%{obsapidir}/bin
%{obsapidir}/test
%{obswwwdir}/docs
%dir %{obsapidir}/config
%{obsapidir}/config/locales
%dir %{obsapidir}/vendor
%{obsapidir}/vendor/diststats
%{obsapidir}/config/boot.rb
%{obsapidir}/config/routes.rb
%{obsapidir}/config/environments/development.rb
%{obsapidir}/config/unicorn
%attr(0644,root,%apache_group) %config(noreplace) %{obsapidir}/config/database.yml*
%attr(0644,root,root) %config(noreplace) %{obsapidir}/config/options.yml*
%dir %attr(0755,%apache_user,%apache_group) %{obsapidir}/db/sphinx
%dir %attr(0755,%apache_user,%apache_group) %{obsapidir}/db/sphinx/production
%{obsapidir}/.bundle
%config %{obsapidir}/config/environment.rb
%config %{obsapidir}/config/environments/production.rb
%config %{obsapidir}/config/environments/test.rb
%config %{obsapidir}/config/environments/stage.rb
%dir %attr(-,%{apache_user},%{apache_group}) %{obsapidir}/log
%attr(-,%{apache_user},%{apache_group}) %{obsapidir}/tmp
# Keep or remove?
%{obsapidir}/api_development
%{obsapidir}/api_test
%{obsapidir}/log/development.log
%config(noreplace) %{_sysconfdir}/httpd/conf.d/obs.conf
# %ghost?
%{obsapidir}/log/access.log
%{obsapidir}/log/backend_access.log
%{obsapidir}/log/delayed_job.log
%{obsapidir}/log/error.log
%{obsapidir}/log/lastevents.access.log
%{obsapidir}/log/production.log

%files -n obs-selinux
# SELinux
#%%doc selinux/*
%{_datadir}/selinux/*/%{modulename}.pp

%files -n obs-utils
%defattr(-,root,root)
%{_sbindir}/obs_project_update

%files -n obs-productconverter
%defattr(-,root,root)
%{_bindir}/obs_productconvert
%{obsserverdir}/bs_productconvert

%files -n obs-devel
%defattr(-,root,root)
%_docdir/README.devel

%changelog
* Mon Dec 08 2014 Josef Stribny - 2.5.50.git3647e3-4
- Move SELinux stuff into its own sub-package

* Mon Dec 08 2014 Josef Stribny - 2.5.50-3
- rebuilt


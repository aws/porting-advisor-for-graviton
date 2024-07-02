import io
import unittest
from os import path
from src.advisor.manifester.dependency import Dependency
from src.advisor.manifester.manifester import Manifester


class TestManifester(unittest.TestCase):
    def test_initialization_loads_rules_correctly(self):
        manifester = Manifester()
        self.assertGreater(len(manifester._supported_files), 0)
        self.assertTrue("requirements.txt" in manifester._supported_files)
        self.assertTrue("pom.xml" in manifester._supported_files)
        self.assertTrue("go.mod" in manifester._supported_files)

    def test_get_dependencies_for_pip_returns_array_of_dependencies(self):
        manifester = Manifester()
        io_object = io.StringIO('''
SciPy == 1.7.2
Jinja2==3.1.2''')
        dependencies = manifester.get_dependencies('requirements.txt', io_object)
        self.assertEqual(2, len(dependencies))
        self.assertEqual('Jinja2', dependencies[1].name)
        self.assertEqual('3.1.2', dependencies[1].version)
        self.assertEqual('requirements.txt', dependencies[1].filename)
        self.assertEqual('pip', dependencies[1].tool)
        self.assertEqual(3, dependencies[1].lineno)

    def test_get_dependencies_for_maven_returns_array_of_dependencies(self):
        manifester = Manifester()
        io_object = io.StringIO(r'''<project>
  <artifactId>my-test1</artifactId>
  <version>1.0</version>
  <properties>
    <snappy.version>1.1.3</snappy.version>
  </properties>
  
  <dependencies>
    <dependency>
      <groupId>org.xerial.snappy</groupId>
      <artifactId>snappy-java</artifactId>
      <version>${snappy.version}</version>
    </dependency>
  </dependencies>
</project>
        ''')
        dependencies = manifester.get_dependencies('pom.xml', io_object)
        self.assertEqual(1, len(dependencies))
        self.assertEqual('snappy-java', dependencies[0].name)
        self.assertEqual('1.1.3', dependencies[0].version)
        self.assertEqual('pom.xml', dependencies[0].filename)
        self.assertEqual('maven', dependencies[0].tool)
    
    def test_get_dependencies_for_go_returns_array_of_dependencies(self):
        manifester = Manifester()
        io_object = io.StringIO('''module sample/graviton-invalid

go 1.18

require (
	github.com/golang/snappy v0.0.2
)''')
        dependencies = manifester.get_dependencies('go.mod', io_object)
        self.assertEqual(1, len(dependencies))
        self.assertEqual('github.com/golang/snappy', dependencies[0].name)
        self.assertEqual('0.0.2', dependencies[0].version)
        self.assertEqual('go.mod', dependencies[0].filename)
        self.assertEqual('go', dependencies[0].tool)
    
    def test_get_dependencies_for_npm_returns_array_of_dependencies(self):
        manifester = Manifester()
        io_object = io.StringIO('''{
  "name": "fakelibraryjs",
  "version": "1.2.3",
  "description": "Test package.json file",
  "scripts": {
    "build": "npm build"
  },
  "dependencies": {
    "cors": "2.8.5",
    "express": "4.18.1",
    "rxjs": "7.5.6",
    "socket.io": "4.5.1",
    "tslib": "2.4.0"
  },
  "devDependencies": {
    "@codechecks/client": "0.1.12",
    "@commitlint/cli": "17.0.3",
    "eslint": "7.32.0",
    "typescript": "4.7.4"
  }
}''')
        dependencies = manifester.get_dependencies('package.json', io_object)
        self.assertEqual(9, len(dependencies))
        self.assertEqual('cors', dependencies[0].name)
        self.assertEqual('2.8.5', dependencies[0].version)
        self.assertEqual('package.json', dependencies[0].filename)
        self.assertEqual('npm', dependencies[0].tool)

    def test_get_dependencies_for_nuget_returns_array_of_dependencies(self):
        manifester = Manifester()
        io_object = io.StringIO('''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Logging.Console" Version="6.0.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="16.5.0" />
    <PackageReference Include="xunit" Version="2.4.1" />
    <PackageReference Include="coverlet.collector" Version="1.2.0" />
  </ItemGroup>

</Project>''')
        dependencies = manifester.get_dependencies('sampledotnet.csproj', io_object)
        self.assertEqual(4, len(dependencies))
        self.assertEqual('Microsoft.Extensions.Logging.Console', dependencies[0].name)
        self.assertEqual('6.0.0', dependencies[0].version)
        self.assertEqual('sampledotnet.csproj', dependencies[0].filename)
        self.assertEqual('nuget', dependencies[0].tool)

    def test_get_dependencies_for_ruby_returns_array_of_dependencies(self):
        manifester = Manifester()
        io_object = io.StringIO('''source 'https://rubygems.org'

gem 'rails', '~> 6.1.6.1'
gem "rake", ">= 11.1"
gem 'actionpack', rails_version
gem 'bcrypt', '~> 3.1', '>= 3.1.14'
gem "cucumber", RUBY_VERSION >= "2.5" ? "~> 5.1.2" : "~> 4.1"
gem 'gc_tracer', require: false, platform: :mri
gem 'gssapi', group: :kerberos
gem 'mail', git: 'https://github.com/discourse/mail.git'
gem "turbo-rails"

group :test do
    gem "httpclient"
    
    if RUBY_ENGINE == "jruby"
      gem "jruby-openssl"
    end
end''')
        dependencies = manifester.get_dependencies('Gemfile', io_object)
        self.assertEqual(11, len(dependencies))
        self.assertEqual('rails', dependencies[0].name)
        self.assertEqual('6.1.6.1', dependencies[0].version)
        self.assertEqual('Gemfile', dependencies[0].filename)
        self.assertEqual('ruby', dependencies[0].tool)
    
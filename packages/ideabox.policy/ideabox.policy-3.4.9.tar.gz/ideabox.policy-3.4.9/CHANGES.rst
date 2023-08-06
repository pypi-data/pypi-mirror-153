Changelog
=========


3.4.9 (2022-06-02)
------------------

- Add endpoints to get projects themes and projects districts
  [boulch]

- Refactor default_image project and take project leadimage in consideration
  [boulch]

- Add map and coordinates in project template
  [boulch]


3.4.8 (2022-06-01)
------------------

- Add new geolocated faceted view
  [boulch]

- Add geolocation field to project content type
  [boulch]

- Move project_image (leadimage) to project content type
  [boulch]

- Adapt code to sort priority action progress by latest to oldest elements
  [mpeeters]


3.4.7 (2022-05-06)
------------------

- Fix js error : Uncaught ReferenceError: ploneFormTabbing is not defined
  [boulch]

- Avoid a double translation for localized month
  [mpeeters]

- auto-install imio.gdpr , collective.excelexport
  [boulch]


3.4.6 (2022-03-08)
------------------

- Fix bad include instruction
  [boulch]


3.4.5 (2022-02-28)
------------------

- Add collective.big.bang dependency
  [boulch]


3.4.4 (2022-02-25)
------------------

- Add package : collective.anonymouseditpatterns. Fix some widgets
  In our case, fix datetime picker in @@register form (in anonymous mode)
  [boulch]


3.4.3 (2021-06-28)
------------------

- Update faceted xml configuration. Add a workflow "draft" filter on projects. (Don't keep projects in draft state)
  [boulch]
- Add a project_directly_submitted checkbox field in ideabox controlpanel to choice is project can be directly submitted
  [boulch]
- Add campaign_emails field on campaign type to send mails only on to these campaign managers
  [boulch]


3.4.2 (2021-06-10)
------------------

- Change "zip_code" field label to "zip code / locality" in user registration form.
  [boulch]


3.4.1 (2021-06-09)
------------------

- Create legal_information_text field in control panel
  [boulch]


3.4.0 (2021-02-03)
------------------

- Add REST API specific viewlets on prioity action template
  [mpeeters]
- Change two taxonomies title (locality, district)
  [boulch]
- undo description for "birthdate" field in registration form (calendar widget up again)
  [boulch]
- Fix typo in js compilation filename
  [mpeeters]
- Add description for "birthdate" field in registration form
- [SUP-14825] Add description for "birthdate" field in registration form
  [boulch]
- Add some translations
  [boulch]


3.3.1 (2020-09-10)
------------------

- Fix encoding issue in faceted tests.
  [boulch]
- [IDBOX-22] : Add locality taxonomy and use it instead of vocabulary for user zip_code field + upgrade step (create taxonomy).
  [boulch]


3.3.0 (2020-08-28)
------------------

- Fix an issue with faceted view used on Folder
  [mpeeters]

- Add newsletter tile
  [vpiret]


3.2.0 (2020-08-20)
------------------

- Fix an error during registration of users
  [mpeeters]

- [IDBOX-25] : Move disable/enable project submission from registry to a field in each Campaign.
  [boulch]

- [IDBOX-25] : Add "Create project" button on campaign.
  [boulch]


3.1.3 (2020-08-04)
------------------

- Add image on news
  [mpeeters]


3.1.2 (2020-08-04)
------------------

- Cleanup actuality facete code
  [vpiret]

- Add publication date on news items view
  [vpiret]

- Add publication date on actuality facete
  [vpiret]


3.1.1 (2020-06-30)
------------------

- Disable subscription button since developments are not ready
  [mpeeters]


3.1.0 (2020-06-29)
------------------

- Change news faceted item structure for redesign
  [mpeeters]

- Add missing pickadate js resource for anonymous
  [mpeeters]

- Use request as context to translate month in dates
  [mpeeters]

- Remove description from tile on news faceted
  [mpeeters]


3.1.0a11 (2020-06-28)
---------------------

- Fix translation of state progress date on progress view
  [mpeeters]

- Add the project title on the progress view
  [mpeeters]

- Allow `Folder` and `Link` on `Campaign` content type
  [mpeeters]

- Add a link to all progress view on project progress title
  [mpeeters]

- Remove strategic and operational objectives from project faceted view
  [mpeeters]

- Fix campaign faceted view
  [mpeeters]

- Always display the column with progress for priority actions and add a message when there is no progress
  [mpeeters]


3.1.0a10 (2020-06-26)
---------------------

- Add login popup in action view
  [Aurore]

- Change condition for image in action view
  [Aurore]

- Add missing translated texts
  [mpeeters]

- Add a parameter to priority action tiles to specify from which folder or campaign the actions should be displayed
  [mpeeters]

- Add a Random Priority Actions tile
  [mpeeters]

- Add legal terms on register form
  [mpeeters]

- Allow to create `Campaign` in `Campaign` content type to handle subcampaign mecanism
  [mpeeters]

- Fix display of campaign images on projects and actions
  [mpeeters]

- Add missing translations
  [mpeeters]

- Translate month in dates
  [mpeeters]


3.1.0a9 (2020-06-24)
--------------------

- Add class pat-moment on state_progress dates
  [vpiret]


3.1.0a8 (2020-06-23)
--------------------

- Fix random sort mecanism
  [mpeeters]

- Fix image on actions view
  [Aurore]


3.1.0a7 (2020-06-23)
--------------------

- Add an upgrade step for the new content types
  [mpeeters]

- Fix allowed types for campaign and add excludefromnavigation behavior
  [mpeeters]


3.1.0a6 (2020-06-22)
--------------------

- Adapt template for state actions
  [Aurore]

- Add `ideabox.restapi` dependency
  [mpeeters]

- District and theme are now optional for project and priority action and are now display only if a value is defined
  [mpeeters]


3.1.0a5 (2020-06-22)
--------------------

- Adapt image for project view
  [Aurore]

- Adapt title for homepage
  [Aurore]

- Override priority_action schema
  [vpiret]

- Add macaron
  [vpiret]

- Add content type "campaign"
  [vpiret]

- Fix display of state_progress
  [vpiret]


3.1.0a4 (2020-06-12)
--------------------

- Move comments viewlet into `plone.belowcontentbody` manager
  [mpeeters]

- Fix duplicate comments due to a duplicate render of `viewlet-below-content` that was introduce by Plone 5.2
  [mpeeters]


3.1.0a3 (2020-06-11)
--------------------

- Fix encoding of `SearchableText` index on Python 3
  [mpeeters]

- Fix encoding for comments with Python 3
  [mpeeters]


3.1.0a2 (2020-06-11)
--------------------

- Add translation
  [vpiret]

- Add priority action tiles
  [vpiret, Aurore]

- Transforms the display of project themes to links
  [vpiret]

- Add StateProgress view
  [vpiret]


3.1.0a1 (2020-06-09)
--------------------

- Restore district informations for projects that are now conditional
  [mpeeters]

- Adapt action and project view
  [Aurore]

- Fix a Python 3 encoding issue on project tile
  [mpeeters]

- Restore initial config on install
  [mpeeters]

- Fix Python3 compability
  [mpeeters]

- Restore `imio.gdpr` dependency
  [mpeeters]

- Restore beaker dependency
  [mpeeters]

- Add new content "State progress"
  [vpiret]

- Adapte faceted navigation with new fields
  [vpiret]

- Add new content "Priority action"
  [vpiret]

- Handle optional random sort for projects by using a new sort widget
  [mpeeters]

- Add a sorting faceted widget that allow sort on every index and does not have Relevance by default
  [mpeeters]

- Add `ideabox.vocabularies.sort_project` vocabulary for faceted sorting projects options
  [mpeeters]

- Add `ideabox.stats` to the package dependencies
  [mpeeters]

- Fix an encoding issue with md5 on Python 3 for random sort
  [mpeeters]

- Fix an issue with `project_district` index and Python 3
  [mpeeters]


3.0.7 (2020-02-20)
------------------

- Improve projet SearchableText.
  [bsuttor]


3.0.6 (2020-02-20)
------------------

- First step of migrate code to python 3.
  [bsuttor]


3.0.5 (2020-02-20)
------------------

- Remove old dependencies.
  [bsuttor]


3.0.4 (2020-02-19)
------------------

- Remove specific installation.
  [bsuttor]


3.0.3 (2020-02-19)
------------------

- Clean up registry.
  [bsuttor]


3.0.2 (2020-02-19)
------------------

- Clean up metadata.xml profile.
  [bsuttor]


3.0.1 (2020-02-19)
------------------

- Remove <include package="Products.BeakerSessionDataManager" /> from configure.
  [bsuttor]


3.0.0 (2020-02-19)
------------------

- Remove beaker dependency.
  [bsuttor]

- Do not install a theme by default
  [mpeeters]

- Add ideabox.theme dependency
  [mpeeters]


2.3.7 (2019-10-10)
------------------

- Handle basic html structure in timeline tile titles
  [mpeeters]


2.3.6 (2019-06-30)
------------------

- Update collection separator for export
  [vpiret, mpeeters]


2.3.5 (2019-06-24)
------------------

- Add separator in export users
  [vpiret]


2.3.4 (2019-06-24)
------------------

- Fix typo
  [mpeeters]


2.3.3 (2019-06-24)
------------------

- Add status message for vote encoding
  [vpiret]


2.3.2 (2019-06-24)
------------------

- Add vote encoding form
  [vpiret]


2.3.1 (2019-06-12)
------------------

- Fix user names displayed on comments (it was the email address)
  [mpeeter]


2.3.0 (2019-06-09)
------------------

- Add a tile to randomly display projects
  [mpeeter]


2.2.0 (2019-06-06)
------------------

- Improve random sort of projects
  [mpeeters]

- Fix social media metadatas for projects
  [mpeeters]


2.1.4 (2019-05-28)
------------------

- Remove user votes on export excel
  [vpiret]


2.1.3 (2019-05-27)
------------------

- Add negative rating on export excell
  [vpiret]


2.1.2 (2019-05-03)
------------------

- `address` is no longer a required field
  [mpeeters]

- Fix project_encoding if the mail is too long
  [vpiret]


2.1.1 (2019-04-22)
------------------

- Fix faceted query and batch for projects
  [mpeeters]


2.1 (2019-04-16)
----------------

- Fix export of users
  [vpiret, mpeeters]

- Adapt required fields for project encoding form
  [mpeeters]

- Add address property members
  [vpiret, mpeeters]

- Implement number_of_projects_displayed
  [vpiret]


2.0b6 (2019-04-03)
------------------

- Add Products.BeakerSessionDataManager
  [mpeeters]

- Add enable / disable project submission
  [vpiret]

- Remove description field on project
  [mpeeters]

- Add permission for export projects and users
  [vpiret]

- Add action user for excel export
  [vpiret]

- Fix the excel export and appends the "I am" field
  [vpiret]


2.0b5 (2019-04-02)
------------------

- Fix project faceted navigation
  [mpeeters]


2.0b4 (2019-04-02)
------------------

- Fix project_encoding
  [vpiret]

- Fix project workflow
  [vpiret]

- Implement project_encoding
  [vpiret]

- Add a faceted view for events
  [mpeeters]

- Add plone.app.imagecropping to the package dependencies
  [mpeeters]

- Add the missing `evenement` scale
  [mpeeters]

- Add a default image for project view
  [mpeeters]


2.0b3 (2019-04-01)
------------------

- Revert removing pas.plugins.imio from package dependencies
  [mpeeters]


2.0b2 (2019-04-01)
------------------

- Upgade i am vocabulary
  [vpiret]


2.0b1 (2019-03-31)
------------------

- Do not display elements that are excluded from navigation on summary and listing views
  [mpeeters]

- Add collective.disclaimer to the package dependencies
  [mpeeters]

- Add `I am` user field
  [mpeeters]

- Rename the lastname title to include institution
  [mpeeters]

- The user firstname is now optional
  [mpeeters]

- Fix control panel form name
  [mpeeters]

- Fix project district filter on faceted navigation
  [mpeeters]


2.0a12 (2019-03-28)
-------------------

- Remove pas.plugins.imio since WC will not be available for the first release
  [mpeeters]

- Add legal informations under the project submission form
  [mpeeters]

- Fix an error during project indexing
  [mpeeters]

- Add button to projects tile
  [Aurore]

- Adapt timeline tile
  [Aurore]


2.0a11 (2019-03-28)
-------------------

- adapte SearchableText for adding body project
  [vpiret]

- Upgrade faceted config for project
  [vpiret]

- Fix district on project submision
  [vpiret]


2.0a10 (2019-03-23)
-------------------

- Update fields titles and requirements
  [vpiret]

- Update zip code vocabulary
  [vpiret]

- Change title field project
  [vpiret]

- Add export projects and users
  [vpiret]

- Use Black python formatter
  [mpeeters]


2.0a9 (2019-03-09)
------------------

- Simplify creation of project objects during submission
  [mpeeters]

- Fix typo in control panel values
  [mpeeters]


2.0a8 (2019-03-09)
------------------

- Fix banner image size
  [mpeeters]

- Fix the display of authors names
  [mpeeters]

- Add a permission to protect project submission
  [mpeeters]

- Avoid an error if the notification email is not defined
  [mpeeters]


2.0a7 (2019-03-04)
------------------

- Fix theme vocabulary on project view
  [mpeeters]

- Remove ratings from states before voting
  [mpeeters]

- Add new translation
  [vpiret]

- Send email on new project submission
  [vpiret]


2.0a6 (2019-03-04)
------------------

- Change permission for show toolbar
  [amariscal]

- Correctly get the themes in latest projects tile
  [mpeeters]

- Use the extended user schema for subscription
  [mpeeters]

- Add taxonomies and configuration
  [vpiret, mpeeters]

- Auto publish default contents
  [mpeeters]

- Deactivate the portlets columns on some contents
  [mpeeters]

- Update the default contents on install
  [mpeeters]

- Add the faceted navigation for news
  [mpeeters]

- Set the default values for the menu
  [mpeeters]

- Add Products.PasswordStrength and imio.gdpr to the dependencies
  [mpeeters]

- Activate the subscription for users
  [mpeeters]

- Add portal-footer
  [amariscal]


2.0a5 (2019-02-26)
------------------

- Add pas.plugins.imio dependency.
  [bsuttor]


2.0a4 (2019-02-23)
------------------

- Update the default rating states
  [mpeeters]

- Update the themes
  [mpeeters]

- Add timeline tile and rename file
  [amariscal]

- Fix CSRF issue with comments auto enabled
  [mpeeters]

- Adapt the tile for the latest projects
  [mpeeters]

- Adapt the display of project themes in faceted view
  [mpeeters]

- Fix the registration of new allowed sizes
  [mpeeters]

- Add the `project_faceted` scale on install
  [mpeeters]

- Adapt template for menu user
  [Aurore]

- Adapt tile for projects
  [Aurore]

- Add default faceted configuration for projects
  [vpiret]

- Fix project for export data
  [vpiret]

- Upgrade members data schema
  [vpiret]

- Add ideabox.diazotheme.spirit to the package dependencies
  [Aurore]

- Fix tile for projects
  [mpeeters]

- Add iaweb.mosaic to the package dependencies
  [mpeeters]

- Send mail on project submission
  [vpiret]

- Add behavior banner on Folder and Page
  [vpiret]

- Add rating on faceted view
  [vpiret]

- Configure beahavior banner
  [vpiret]


2.0a3 (2019-01-31)
------------------

- Add test robot for project submission
  [vpiret]

- Add collective.behavior.banner to the package dependencies
  [mpeeters]

- Add transition for project submission
  [vpiret]

- Add collective.editablemenu on dependencies
  [vpiret]

- Fix buildout for travis
  [vpiret]

- Add user menu for personal information
  [vpiret]


2.0a2 (2019-01-28)
------------------

- Fix project for plone 5
  [vpiret]


2.0a1 (2019-01-28)
------------------

- Removal of cpskin dependencies for Plone 5 transition
  [daggelpop]

- Upgrade project fields
  [vpiret]

- Add project_submission form for connected users
  [vpiret]


1.0.3 (2018-07-23)
------------------

- Fix project summary view
  [vpiret]

- Fix templates for showing map
  [vpiret, mpeeters]

- add dependency export excel
  [vpiret]


1.0.2 (2018-07-16)
------------------

- Add `imio.gdpr` to the dependencies
  [mpeeters]

- Change link on element of homepage
  [Aurore]

- Sort links by priority
  [vpiret]


1.0.1 (2018-04-07)
------------------

- Fix release
  [mpeeters]


1.0 (2018-04-07)
----------------

- Add default image on project faceted view
  [mpeeters]

- Add a summary view by theme
  [mpeeters]

- Hide the timeline on projects
  [mpeeters]

- Add collective.behavior.richdescription to the package dependencies
  [mpeeters]


1.0a8 (2018-04-03)
------------------

- Test permissions on the current user
  [mpeeters]


1.0a7 (2018-03-29)
------------------

- Do not display the news tab when there is no news
  [mpeeters]

- Do not display the votes on selected projects
  [mpeeters]


1.0a6 (2018-03-28)
------------------

- Add pas.plugins.imio dependency.
  [bsuttor]


1.0a5 (2018-03-27)
------------------

- Add a view for the projects summary
  [mpeeters]

- Add more transitions in project workflow to be more explicit
  [mpeeters]

- Add a vocabulary for project states
  [mpeeters]

- Improve project view
  [mpeeters]


1.0a4 (2018-03-26)
------------------

- Add a view to edit workflow dates
  [mpeeters]

- Allow more states for social viewlet
  [mpeeters]

- Update project template to include `plone.abovecontenttile`
  and `plone.belowcontenttile` viewlet managers
  [mpeeters]

- Store the image reference on the project for sliders
  [mpeeters]


1.0a3 (2018-03-25)
------------------

- Randomize the order of items in projects faceted view
  [mpeeters]

- Always allow discussion on projects (78 minutes ago)
  [mpeeters]

- Invert theme and title in projects faceted view
  [mpeeters]

- Fix background for projects in faceted view
  [mpeeters]

- Improve project import script
  [mpeeters]

- Add tabs on project view
  [amariscal, mpeeters]

- Handle `.png` and `.gif` in project import script
  [vpiret]

- Improve timeline design
  [amariscal, mpeeters]


1.0a2 (2018-03-18)
------------------

- Configure plone.app.discussion for projects
  [mpeeters]

- Customize the rating view
  [mpeeters]

- Implement the timeline
  [vpiret, mpeeters]

- Implement the view for projects
  [vpiret, amariscal, mgennart, mpeeters]

- Add the faceted view for projects
  [mpeeters]

- Improve import scripts
  [vpiret]

- Add translation
  [vpiret, mpeeters]


1.0a1 (2018-03-05)
------------------

- Initial release.
  [mpeeters, vpiret, amariscal, mgennart]

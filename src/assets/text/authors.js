export default {
    // Do not update title w/o checking with Cee/Hayley - we want this to be consistent across sites
    title: "USGS Vizlab",
    // Do not update lead text w/o checking with Cee/Hayley - we want this to be consistent across sites
    leadText: "This site was created by the <a href='https://labs.waterdata.usgs.gov/visualizations/' target='_blank'>USGS Vizlab</a>. ",
    // in-between text elements specified here, to avoid hard-coding in `AuthorshipSection.vue`
    conjunctionWord: "and",
    leadPhrase: "led the project",
    contributionsPhrase: "with contributions from",
    // do not delete section. delete individuals as needed. modify content as needed
    // currently only 'fullName', 'firstName', 'initials', 'profile_link', and 'contribution' are used
    primaryAuthors: [
      {
        firstName: 'Jeffrey',
        lastName: 'Kwang',
        fullName: 'Jeffrey Kwang',
        initials: 'JK',
        profile_link: 'https://www.usgs.gov/staff-profiles/jeffrey-kwang',
        role: 'lead',
        contribution: 'created data visualizations'
      }
    ],
    // do not delete section. delete any or all individuals as needed. modify content as needed
    // currently only 'fullName', 'firstName', 'initials', 'profile_link', and 'contribution' are used
    additionalAuthors: [
      {
        firstName: 'Cee',
        lastName: 'Nell',
        fullName: 'Cee Nell',
        initials: 'CN',
        profile_link: 'https://www.usgs.gov/staff-profiles/cee-nell',
        role: 'team lead',
        contribution: 'lead the project'
      },
      {
        firstName: 'Hayley',
        lastName: 'Corson-Dosch',
        fullName: 'Hayley Corson-Dosch',
        initials: 'HCD',
        profile_link: 'https://www.usgs.gov/staff-profiles/hayley-corson-dosch',
        
        role: 'developer',
        contribution: 'built the structure of the website and reviewed code'
      },
      {
        firstName: 'Jeremy',
        lastName: 'Diaz',
        fullName: 'Jeremy Diaz',
        initials: 'JD',
        profile_link: null,
        role: 'SME',
        contribution: 'provided subject matter expertise on modeling and uncertainty quantification'
      }
    ]
};
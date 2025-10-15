import { trigger, transition, style, animate, query, group, animateChild } from '@angular/animations';

// Fade in/out simple
export const fadeInOut = trigger('fadeInOut', [
  transition(':enter', [
    style({ opacity: 0 }),
    animate('300ms ease-in', style({ opacity: 1 }))
  ]),
  transition(':leave', [
    animate('300ms ease-out', style({ opacity: 0 }))
  ])
]);

// Slide vertical
export const slideIn = trigger('slideIn', [
  transition(':enter', [
    style({ transform: 'translateY(10px)', opacity: 0 }),
    animate('300ms ease-out', style({ transform: 'translateY(0)', opacity: 1 }))
  ]),
  transition(':leave', [
    animate('300ms ease-in', style({ transform: 'translateY(10px)', opacity: 0 }))
  ])
]);

// Slide horizontal gauche/droite
export const slideHorizontal = trigger('slideHorizontal', [
  transition(':enter', [
    style({ transform: 'translateX(-100%)', opacity: 0 }),
    animate('400ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
  ]),
  transition(':leave', [
    animate('400ms ease-in', style({ transform: 'translateX(-100%)', opacity: 0 }))
  ])
]);

// Zoom (scale in/out)
export const zoomInOut = trigger('zoomInOut', [
  transition(':enter', [
    style({ transform: 'scale(0.8)', opacity: 0 }),
    animate('300ms ease-out', style({ transform: 'scale(1)', opacity: 1 }))
  ]),
  transition(':leave', [
    animate('300ms ease-in', style({ transform: 'scale(0.8)', opacity: 0 }))
  ])
]);

// Collapse vertical (hauteur 0 -> auto)
export const collapseVertical = trigger('collapseVertical', [
  transition(':enter', [
    style({ height: '0', overflow: 'hidden', opacity: 0 }),
    animate('100ms ease-out', style({ height: '*', opacity: 1 }))
  ]),
  transition(':leave', [
    animate('100ms ease-in', style({ height: '0', opacity: 0 }))
  ])
]);

// Rotation
export const rotateInOut = trigger('rotateInOut', [
  transition(':enter', [
    style({ transform: 'rotate(-90deg)', opacity: 0 }),
    animate('300ms ease-out', style({ transform: 'rotate(0)', opacity: 1 }))
  ]),
  transition(':leave', [
    animate('300ms ease-in', style({ transform: 'rotate(-90deg)', opacity: 0 }))
  ])
]);

export const rotateInRight = trigger('rotateInRight', [
  transition(':enter', [
    style({ transform: 'rotate(-90deg)', opacity: 0.5 }),
    animate('300ms ease-out', style({ transform: 'rotate(0)', opacity: 1 }))
  ]),
]);

export const rotateInLeft= trigger('rotateInLeft', [
  transition(':enter', [
    style({ transform: 'rotate(90deg)', opacity: 0.5 }),
    animate('300ms ease-out', style({ transform: 'rotate(0)', opacity: 1 }))
  ]),
]);


// Flip horizontal (utile pour cartes)
export const flipInOut = trigger('flipInOut', [
  transition(':enter', [
    style({ transform: 'rotateY(90deg)', opacity: 0 }),
    animate('300ms ease-out', style({ transform: 'rotateY(0)', opacity: 1 }))
  ]),
  transition(':leave', [
    animate('300ms ease-in', style({ transform: 'rotateY(90deg)', opacity: 0 }))
  ])
]);

export const delayedFadeIn = trigger('delayedFadeIn', [
    transition(':enter', [
      style({ opacity: 0 }),
      animate('600ms 300ms ease-in', style({ opacity: 1 }))
    ])
]);

  export const slideUp = trigger('slideUp', [
    transition(':enter', [
      style({ transform: 'translateY(100%)', opacity: 0 }),
      animate('400ms ease-out', style({ transform: 'translateY(0)', opacity: 1 }))
    ]),
    transition(':leave', [
      animate('400ms ease-in', style({ transform: 'translateY(100%)', opacity: 0 }))
    ])
  ]);

  export const pop = trigger('pop', [
    transition(':enter', [
      style({ opacity: 0, transform: 'scale(0.95) translateY(10px)' }),
      animate('250ms ease-out', style({ opacity: 1, transform: 'scale(1) translateY(0)' }))
    ]),
    transition(':leave', [
      animate('250ms ease-in', style({ opacity: 0, transform: 'scale(0.95) translateY(10px)' }))
    ])
  ]);

  export const popIn = trigger('popIn', [
    transition(':enter', [
      style({ opacity: 0, transform: 'scale(0.95) translateY(10px)' }),
      animate('250ms ease-out', style({ opacity: 1, transform: 'scale(1) translateY(0)' }))
    ]),
  ]);

  export const bounceIn = trigger('bounceIn', [
    transition(':enter', [
      style({ transform: 'scale(0.7)', opacity: 0 }),
      animate('300ms cubic-bezier(0.68, -0.55, 0.27, 1.55)', 
        style({ transform: 'scale(1)', opacity: 1 }))
    ])
  ]);

  export const fadeLoop = trigger('fadeLoop', [
    transition('* => *', [
      animate('1000ms ease-in-out', style({ opacity: 0.3 })),
      animate('1000ms ease-in-out', style({ opacity: 1 }))
    ])
  ]);

  export const collapseHorizontal = trigger('collapseHorizontal', [
    transition(':enter', [
      style({ width: '0', opacity: 0, overflow: 'hidden' }),
      animate('300ms ease-out', style({ width: '*', opacity: 1 }))
    ]),
    transition(':leave', [
      animate('300ms ease-in', style({ width: '0', opacity: 0 }))
    ])
  ]);

  export const wipeIn = trigger('wipeIn', [
    transition(':enter', [
      style({ width: '0px', opacity: 0 }),
      animate('500ms ease-out', style({ width: '*', opacity: 1 }))
    ]),
    transition(':leave', [
        animate('400ms ease-in', style({ width: '0', opacity: 0 }))
      ])
  ]);

  export const dropTop = trigger('dropTop', [
    transition(':enter', [
      style({ transform: 'translateY(-200px)', opacity: 0 }),
      animate('200ms cubic-bezier(0.23, 1, 0.32, 1)', style({ transform: 'translateY(0)', opacity: 1 }))
    ]),
    transition(':leave', [
        animate('200ms ease-in', style({ transform: 'translateY(-200px)', opacity: 0 }))
      ])
  ]);

  export const dropBottom = trigger('dropBottom', [
    transition(':enter', [
      style({ transform: 'translateY(200px)', opacity: 0 }),
      animate('300ms cubic-bezier(0.23, 1, 0.32, 1)', style({ transform: 'translateY(0)', opacity: 1 }))
    ]),
    transition(':leave', [
        animate('200ms ease-in', style({ transform: 'translateY(200px)', opacity: 0 }))
      ])
  ]);

  export const shake = trigger('shake', [
    transition(':enter', [
      style({ transform: 'translateX(0)' }),
      animate('300ms', style({ transform: 'translateX(-10px)' })),
      animate('300ms', style({ transform: 'translateX(10px)' })),
      animate('300ms', style({ transform: 'translateX(0)' }))
    ])
  ]);

  export const flash = trigger('flash', [
    transition(':enter', [
      style({ opacity: 0 }),
      animate('100ms', style({ opacity: 1 })),
      animate('100ms', style({ opacity: 0 })),
      animate('100ms', style({ opacity: 1 }))
    ])
  ]);